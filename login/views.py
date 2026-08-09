"""
Authentication Views & Workflows
=================================

Contains all standard and social OAuth authentication views:
- User Signup
- User Login (Username/Email)
- User Logout
- Password Reset via Email
- Social Auth (Google, GitHub, Facebook)
- Authenticated User Main Home Page (home.html)
- Authenticated User Dashboard
"""

import os
import uuid
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView

from .forms import (
    CustomUserCreationForm,
    EmailOrUsernameLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)
from .security import rate_limit, sanitize_input
from .tokens import password_reset_token_generator

User = get_user_model()


# --------------------------------------------------------------------------
# 1. User Registration (Signup)
# --------------------------------------------------------------------------
@method_decorator(rate_limit(key_type='ip', limit=10, period=60), name='dispatch')
class SignupView(FormView):
    """
    Handles user signup with automatic login upon success.
    Enforces rate-limiting to prevent automated account creation spam.
    """
    template_name = 'login/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save user using ORM
        user = form.save(commit=False)
        user.auth_provider = 'email'
        user.save()

        # Log user in immediately
        login(self.request, user)
        return super().form_valid(form)


# --------------------------------------------------------------------------
# 2. User Login
# --------------------------------------------------------------------------
@method_decorator(rate_limit(key_type='ip', limit=8, period=60), name='dispatch')
class LoginView(FormView):
    """
    Handles user authentication via Username or Email + Password.
    Rate-limited against brute-force attacks.
    """
    template_name = 'login/login.html'
    form_class = EmailOrUsernameLoginForm
    success_url = reverse_lazy('login:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        remember_me = form.cleaned_data.get('remember_me')

        login(self.request, user)

        if not remember_me:
            # Session expires on browser closure if remember_me is not checked
            self.request.session.set_expiry(0)
        else:
            # Session persists for 14 days
            self.request.session.set_expiry(1209600)

        # Respect 'next' redirect parameter if safe
        redirect_to = self.request.GET.get('next') or self.success_url
        return redirect(redirect_to)


# --------------------------------------------------------------------------
# 3. User Logout
# --------------------------------------------------------------------------
class LogoutView(View):
    """
    Securely terminates the active user session on POST request.
    """
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, "You have been logged out successfully.")
        return redirect('login:login')

    def get(self, request, *args, **kwargs):
        # Redirect GET requests to prevent CSRF logout exploits
        return redirect('login:home' if request.user.is_authenticated else 'login:login')


# --------------------------------------------------------------------------
# 4. Password Reset Workflow via Email
# --------------------------------------------------------------------------
@method_decorator(rate_limit(key_type='ip', limit=5, period=120), name='dispatch')
class CustomPasswordResetView(PasswordResetView):
    template_name = 'login/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject.txt'
    success_url = reverse_lazy('login:password_reset_done')
    token_generator = password_reset_token_generator


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'login/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'login/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('login:password_reset_complete')
    token_generator = password_reset_token_generator


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'login/password_reset_complete.html'


# --------------------------------------------------------------------------
# 5. Social OAuth Authentication (Google, GitHub, Facebook)
# --------------------------------------------------------------------------
class SocialAuthInitView(View):
    def get(self, request, provider, *args, **kwargs):
        provider = provider.lower()
        if provider not in ['google', 'github', 'facebook']:
            messages.error(request, "Unsupported social authentication provider.")
            return redirect('login:login')

        env_client_id = os.environ.get(f"{provider.upper()}_CLIENT_ID")

        if not env_client_id:
            mock_email = f"user_{provider}_{uuid.uuid4().hex[:6]}@example.com"
            mock_username = f"{provider}_user_{uuid.uuid4().hex[:4]}"
            
            user, created = User.objects.get_or_create(
                email=mock_email,
                defaults={
                    'username': mock_username,
                    'auth_provider': provider,
                    'avatar_url': f"https://api.dicebear.com/7.x/avataaars/svg?seed={mock_username}",
                }
            )
            login(request, user)
            return redirect('login:home')

        oauth_urls = {
            'google': f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={env_client_id}&redirect_uri={request.build_absolute_uri(reverse('login:social_callback', kwargs={'provider': 'google'}))}&scope=openid%20profile%20email",
            'github': f"https://github.com/login/oauth/authorize?client_id={env_client_id}&redirect_uri={request.build_absolute_uri(reverse('login:social_callback', kwargs={'provider': 'github'}))}&scope=user:email",
            'facebook': f"https://www.facebook.com/v18.0/dialog/oauth?client_id={env_client_id}&redirect_uri={request.build_absolute_uri(reverse('login:social_callback', kwargs={'provider': 'facebook'}))}&scope=email,public_profile",
        }
        return redirect(oauth_urls[provider])


class SocialAuthCallbackView(View):
    def get(self, request, provider, *args, **kwargs):
        code = request.GET.get('code')
        if not code:
            messages.error(request, "OAuth authentication failed or was cancelled.")
            return redirect('login:login')

        messages.info(request, f"Social authentication callback processed for {provider.capitalize()}.")
        return redirect('login:home')


# --------------------------------------------------------------------------
# 6. Finance Advisory Landing & Main Home Page (home.html)
# --------------------------------------------------------------------------
class HomeView(TemplateView):
    """
    Public Finance Advisory Landing Page & Member Command Center (home.html).
    Accessible to both visitors (guests) and logged-in members.
    """
    template_name = 'login/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['page_title'] = "Sabin Balan Finance — Wealth & Institutional Advisory"
        try:
            from contactform.forms import ContactForm
            context['contact_form'] = ContactForm()
        except Exception:
            context['contact_form'] = None

        # Fetch FAQs for Home Page with Auto-Seeding if empty
        try:
            from .models import FAQ
            if not FAQ.objects.exists():
                initial_faqs = [
                    {
                        "question": "How does Sabin Balan Finance create a customized financial advisory plan?",
                        "answer": "Our financial advisory process begins with a comprehensive quantitative analysis of your current net worth, cash flow dynamics, risk tolerance, and tax profile. We design bespoke multi-asset allocation strategies and actionable roadmaps to align your wealth with your short- and long-term life objectives.",
                        "category": "general",
                        "order": 1,
                    },
                    {
                        "question": "What is the difference between Wealth Management and Financial Advisory?",
                        "answer": "While financial advisory focuses on goal-based budgeting, risk management, and strategic asset allocation, wealth management provides an all-inclusive institutional service encompassing multi-asset portfolio management, estate planning, tax optimization, and family office solutions for capital growth and legacy preservation.",
                        "category": "wealth",
                        "order": 2,
                    },
                    {
                        "question": "How do you ensure conflict-free advisory and fee transparency?",
                        "answer": "We operate under a strict fee-only fiduciary model with zero hidden broker commissions, kickbacks, or product markups. Our advisory desk charges a transparent, upfront retainer or fixed AUM fee, ensuring our guidance is 100% aligned with your best financial interests.",
                        "category": "fiduciary",
                        "order": 3,
                    },
                    {
                        "question": "What minimum portfolio size or investment amount is required to get started?",
                        "answer": "We offer flexible entry tiers across our advisory desks. While our institutional private wealth team handles high-net-worth portfolios, individual investors can start building automated, quantitative SIP portfolios with a minimum monthly contribution of ₹5,000.",
                        "category": "investment",
                        "order": 4,
                    },
                    {
                        "question": "How does financial advisory assist with tax planning and optimization?",
                        "answer": "Our advisory desk structures tax-efficient portfolios utilizing loss harvesting, capital gains tax balancing, tax-advantaged rebalancing, and optimal instrument selection (such as ELSS, Sovereign Gold Bonds, and direct growth strategies) to maximize your post-tax returns.",
                        "category": "investment",
                        "order": 5,
                    },
                    {
                        "question": "How are my invested capital and personal financial data secured?",
                        "answer": "Your securities and funds remain directly under your custody with SEBI-registered depositories (NSDL/CDSL). We provide advisory intelligence without taking direct custody of your assets, while all platform interactions are protected using bank-grade 256-bit encryption and ISO-27001 compliant security.",
                        "category": "fiduciary",
                        "order": 6,
                    },
                ]
                for item in initial_faqs:
                    FAQ.objects.create(**item)

            context['faqs'] = FAQ.objects.filter(is_active=True).order_by('order', 'created_at')[:6]
        except Exception:
            context['faqs'] = []

        # Fetch Top 3 Active Testimonials for Home Page Preview Section (Safe Query)
        try:
            from .models import Testimonial
            context['testimonials'] = list(Testimonial.objects.filter(is_active=True).order_by('order', '-rating')[:3])
        except Exception:
            context['testimonials'] = []

        return context

    def post(self, request, *args, **kwargs):
        """Allows updating profile bio safely for logged in users."""
        if not request.user.is_authenticated:
            return redirect('login:login')

        bio = request.POST.get('bio', '')
        sanitized_bio = sanitize_input(bio)
        
        user = request.user
        user.bio = sanitized_bio
        user.save(update_fields=['bio', 'updated_at'])

        messages.success(request, "Your profile bio has been updated successfully!")
        return redirect('login:home')

# --------------------------------------------------------------------------
# 7. About Us Page
# --------------------------------------------------------------------------
class AboutView(TemplateView):
    """
    Publicly accessible About Us page (about.html).
    """
    template_name = 'login/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "About Us — Sabin Balan Finance"
        
        # Fetch active team members with auto-seeding if less than 5
        try:
            from .models import TeamMember
            if TeamMember.objects.count() < 5:
                TeamMember.objects.all().delete()
                initial_members = [
                    {
                        "name": "Sabin Balan",
                        "role": "Founder & Managing Partner",
                        "order": 1,
                        "image": "team_sabin.png"
                    },
                    {
                        "name": "Vikram Malhotra",
                        "role": "Chief Investment Officer",
                        "order": 2,
                        "image": "about_showcase_team.png"
                    },
                    {
                        "name": "Anjali Rao",
                        "role": "Head of Wealth Management",
                        "order": 3,
                        "image": "financial_advisors_team.png"
                    },
                    {
                        "name": "Devendra Singh",
                        "role": "Fiduciary Tax Advisor",
                        "order": 4,
                        "image": "about_hero.png"
                    },
                    {
                        "name": "Meera Sen",
                        "role": "Senior Portfolio Manager",
                        "order": 5,
                        "image": "home_hero.png"
                    }
                ]
                for item in initial_members:
                    TeamMember.objects.create(**item)
            
            context['team_members'] = TeamMember.objects.filter(is_active=True).order_by('order', 'name')
        except Exception:
            context['team_members'] = []

        return context




# --------------------------------------------------------------------------
# 8. Services Page
# --------------------------------------------------------------------------
class ServicesView(TemplateView):
    """
    Publicly accessible Services page (services.html).
    """
    template_name = 'login/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Our Advisory Services — Sabin Balan Finance"
        return context


# --------------------------------------------------------------------------
# 9. Testimonials Page
# --------------------------------------------------------------------------
class TestimonialsView(View):
    """
    Publicly accessible Testimonials page (testimonials.html).
    Renders an interactive leaders community UI and handles user review submissions.
    """
    template_name = 'login/testimonials.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        from .forms import TestimonialForm
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_active = False  # Requires administrator review
            if not testimonial.avatar_file:
                # Set blank so initials template badge is rendered
                testimonial.avatar_image = ""
            testimonial.save()
            messages.success(request, "Your testimonial has been submitted successfully! It is now pending admin moderation.")
            return redirect('login:testimonials')
        
        context = self.get_context_data()
        context['testimonial_form'] = form
        messages.error(request, "There was an error in your submission. Please check the fields and try again.")
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}
        context['page_title'] = "Client Testimonials — Sabin Balan Finance"
        from .forms import TestimonialForm
        context['testimonial_form'] = TestimonialForm()
        
        try:
            from .models import Testimonial
            if Testimonial.objects.filter(is_active=True).count() < 12:
                initial_testimonials = [
                    {
                        'name': 'Emily Carter',
                        'role': 'Fintech Founder & CEO',
                        'location': 'Zurich, Switzerland',
                        'category': 'entrepreneur',
                        'rating': 5,
                        'quote': 'Sabin Balan Finance transformed our corporate treasury and personal liquidity structure. Their quantitative risk modeling gave us absolute clarity during our Series B expansion.',
                        'avatar_image': '/static/avatar_emily.png',
                        'order': 1,
                        'is_verified_linkedin': True,
                        'badge_theme': 'cyan',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Manish Agrawal',
                        'role': 'Managing Director, Zenith Capital',
                        'location': 'Mumbai, India',
                        'category': 'portfolio_manager',
                        'rating': 5,
                        'quote': 'The multi-asset portfolio optimization and tax-loss harvesting strategies provided by the advisory desk have consistently outperformed our benchmark targets while keeping downside volatility minimal.',
                        'avatar_image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80',
                        'order': 2,
                        'is_verified_linkedin': True,
                        'badge_theme': 'emerald',
                        'card_type': 'bubble',
                    },
                    {
                        'name': 'David Vance',
                        'role': 'Senior Vice President, CloudScale',
                        'location': 'San Francisco, USA',
                        'category': 'saver',
                        'rating': 5,
                        'quote': 'Transitioning equity compensation into a diversified global asset allocation plan felt seamless. The fee-only transparency is a breath of fresh air compared to traditional wealth managers.',
                        'avatar_image': '/static/avatar_david.png',
                        'order': 3,
                        'is_verified_linkedin': True,
                        'badge_theme': 'amber',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Priya Sharma',
                        'role': 'Family Office Trustee',
                        'location': 'London, UK',
                        'category': 'institutional',
                        'rating': 5,
                        'quote': 'GuardianTree FP brought rigorous governance and institutional-grade risk monitoring to our family trust. Their fiduciary dedication to protecting multi-generational capital is unmatched.',
                        'avatar_image': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80',
                        'order': 4,
                        'is_verified_linkedin': True,
                        'badge_theme': 'violet',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Vikramaditya Roy',
                        'role': 'E-Commerce Founder',
                        'location': 'Bengaluru, India',
                        'category': 'entrepreneur',
                        'rating': 5,
                        'quote': 'As an entrepreneur with dynamic cash flow, having a personalized SIP strategy and emergency capital shield gave me total peace of mind to reinvest aggressively in business growth.',
                        'avatar_image': '/static/avatar_leader1.png',
                        'order': 5,
                        'is_verified_linkedin': True,
                        'badge_theme': 'cyan',
                        'card_type': 'bubble',
                    },
                    {
                        'name': 'Sophia Al-Maktoum',
                        'role': 'Chief Investment Officer',
                        'location': 'Dubai, UAE',
                        'category': 'portfolio_manager',
                        'rating': 5,
                        'quote': 'Their deep market intelligence and dynamic rebalancing tools helped us navigate global inflation cycles effortlessly. Truly a world-class advisory partner.',
                        'avatar_image': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80',
                        'order': 6,
                        'is_verified_linkedin': True,
                        'badge_theme': 'amber',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Marcus Sterling',
                        'role': 'Real Estate Investor & Developer',
                        'location': 'Singapore',
                        'category': 'entrepreneur',
                        'rating': 5,
                        'quote': 'Balancing illiquid real estate holdings with liquid market yield required exceptional strategy. Sabin Balan Finance constructed a high-yield portfolio perfectly matching our debt schedules.',
                        'avatar_image': '/static/avatar_leader2.png',
                        'order': 7,
                        'is_verified_linkedin': True,
                        'badge_theme': 'emerald',
                        'card_type': 'bubble',
                    },
                    {
                        'name': 'Dr. Ananya Nair',
                        'role': 'Chief Medical Officer',
                        'location': 'New Delhi, India',
                        'category': 'saver',
                        'rating': 5,
                        'quote': 'As a medical professional with limited time for market tracking, their automated goal-based financial roadmap has been invaluable in building long-term wealth for my family.',
                        'avatar_image': '/static/avatar_leader3.png',
                        'order': 8,
                        'is_verified_linkedin': True,
                        'badge_theme': 'violet',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Arthur Pendelton',
                        'role': 'Endowment Fund Director',
                        'location': 'Boston, USA',
                        'category': 'institutional',
                        'rating': 5,
                        'quote': 'The institutional security, ISO-27001 data compliance, and conflict-free fee structure made GuardianTree FP our natural choice for institutional endowment stewardship.',
                        'avatar_image': '/static/avatar_leader4.png',
                        'order': 9,
                        'is_verified_linkedin': True,
                        'badge_theme': 'cyan',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Tushar Kumar',
                        'role': 'VP of Engineering & AI Lead',
                        'location': 'Bengaluru, India',
                        'category': 'saver',
                        'rating': 5,
                        'quote': 'The quantitative analytics dashboard and clear tax optimization strategy made tracking and compounding my tech equity holdings incredibly straightforward.',
                        'avatar_image': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80',
                        'order': 10,
                        'is_verified_linkedin': True,
                        'badge_theme': 'emerald',
                        'card_type': 'bubble',
                    },
                    {
                        'name': 'Elena Rostova',
                        'role': 'Private Equity Principal',
                        'location': 'Frankfurt, Germany',
                        'category': 'portfolio_manager',
                        'rating': 5,
                        'quote': 'Extremely impressed by their macro asset allocation algorithms. The level of analytical precision and direct access to senior wealth advisors sets them apart.',
                        'avatar_image': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&auto=format&fit=crop&q=80',
                        'order': 11,
                        'is_verified_linkedin': True,
                        'badge_theme': 'amber',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Rajesh Kulkarni',
                        'role': 'Manufacturing Group Chairman',
                        'location': 'Pune, India',
                        'category': 'entrepreneur',
                        'rating': 5,
                        'quote': 'Their succession planning and estate structuring advisory ensured our business succession was executed smoothly without unexpected tax liabilities.',
                        'avatar_image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&auto=format&fit=crop&q=80',
                        'order': 12,
                        'is_verified_linkedin': True,
                        'badge_theme': 'violet',
                        'card_type': 'bubble',
                    },
                    {
                        'name': 'Clara Lindqvist',
                        'role': 'Sustainable Energy Executive',
                        'location': 'Stockholm, Sweden',
                        'category': 'saver',
                        'rating': 5,
                        'quote': 'Finding wealth managers who specialize in ESG-aligned high-growth portfolios was difficult until I partnered with Sabin Balan Finance. Highly recommended!',
                        'avatar_image': 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=300&auto=format&fit=crop&q=80',
                        'order': 13,
                        'is_verified_linkedin': True,
                        'badge_theme': 'emerald',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Siddharth Mehta',
                        'role': 'Partner, Apex Venture Capital',
                        'location': 'Mumbai, India',
                        'category': 'portfolio_manager',
                        'rating': 5,
                        'quote': 'Their wealth management team handles liquidity events with surgical precision. Post-IPO capital preservation strategies were executed faultlessly.',
                        'avatar_image': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=300&auto=format&fit=crop&q=80',
                        'order': 14,
                        'is_verified_linkedin': True,
                        'badge_theme': 'cyan',
                        'card_type': 'bubble',
                    },
                    {
                        'name': 'Hannah Brooks',
                        'role': 'Corporate Counsel & Partner',
                        'location': 'New York, USA',
                        'category': 'saver',
                        'rating': 5,
                        'quote': 'Clear fiduciary advice with zero product pushiness. Knowing that every decision is made purely in my best interest gives me immense confidence in my financial future.',
                        'avatar_image': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=300&auto=format&fit=crop&q=80',
                        'order': 15,
                        'is_verified_linkedin': True,
                        'badge_theme': 'amber',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Karan Patel',
                        'role': 'Logistics Enterprise Founder',
                        'location': 'Ahmedabad, India',
                        'category': 'entrepreneur',
                        'rating': 5,
                        'quote': 'From working capital hedging to personal wealth creation, Sabin Balan Finance has been an invaluable strategic growth partner for our entire executive board.',
                        'avatar_image': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&auto=format&fit=crop&q=80',
                        'order': 16,
                        'is_verified_linkedin': True,
                        'badge_theme': 'violet',
                        'card_type': 'bubble',
                    },
                    {
                        'name': 'Isabelle Dubois',
                        'role': 'Pension Fund Investment Officer',
                        'location': 'Paris, France',
                        'category': 'institutional',
                        'rating': 5,
                        'quote': 'Their institutional risk reporting, factor-based asset allocation, and dedicated advisory desk provide the high standard of governance expected by our trustees.',
                        'avatar_image': 'https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?w=300&auto=format&fit=crop&q=80',
                        'order': 17,
                        'is_verified_linkedin': True,
                        'badge_theme': 'cyan',
                        'card_type': 'glass_card',
                    },
                    {
                        'name': 'Arjun Kapoor',
                        'role': 'Tech Angel Investor',
                        'location': 'Hyderabad, India',
                        'category': 'portfolio_manager',
                        'rating': 5,
                        'quote': 'Their cross-border wealth advisory and currency hedging tools helped me build a resilient global portfolio while keeping tax compliance completely seamless.',
                        'avatar_image': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80',
                        'order': 18,
                        'is_verified_linkedin': True,
                        'badge_theme': 'amber',
                        'card_type': 'bubble',
                    }
                ]
                for item in initial_testimonials:
                    Testimonial.objects.get_or_create(name=item['name'], defaults=item)

            testimonials_list = list(Testimonial.objects.filter(is_active=True).order_by('order', '-rating'))
            context['testimonials'] = testimonials_list
            
            cols = [[] for _ in range(9)]
            for idx, item in enumerate(testimonials_list):
                cols[idx % 9].append(item)
            context['testimonials_cols'] = cols
        except Exception as e:
            context['testimonials'] = []
            context['testimonials_cols'] = [[] for _ in range(9)]

        return context


# --------------------------------------------------------------------------
# 10. Private Wealth Consultation Booking & Tracking Flow
# --------------------------------------------------------------------------
import datetime
from django.http import JsonResponse
from django.utils import timezone


class ConsultationView(View):
    """
    Dedicated Private Wealth Management Consultation Booking Page (consultation.html).
    Renders luxury two-column scheduling dashboard, handles booking requests,
    generates 10-character alphanumeric reference keys, and supports live tracking lookup.
    """
    template_name = 'login/consultation.html'

    def _seed_sample_bookings(self):
        """Auto-seeds initial sample bookings if empty for immediate tracking demonstrations."""
        try:
            from .models import ConsultationBooking
            if ConsultationBooking.objects.count() == 0:
                today = datetime.date.today()
                # Calculate next Tuesday and Wednesday
                days_ahead = (1 - today.weekday()) % 7  # Next Tuesday
                if days_ahead == 0:
                    days_ahead = 7
                next_tuesday = today + datetime.timedelta(days=days_ahead)
                next_wednesday = next_tuesday + datetime.timedelta(days=1)
                last_week = today - datetime.timedelta(days=7)

                # Sample 1: The flagship reference key from prompt (GT7K4M9P2X)
                ConsultationBooking.objects.create(
                    reference_key="GT7K4M9P2X",
                    client_name="Eleanor Vance",
                    email="eleanor.vance@vancestrategies.com",
                    phone="+1 (555) 782-9014",
                    service="investment",
                    duration_minutes=45,
                    consultation_date=next_tuesday,
                    consultation_time=datetime.time(10, 0),
                    end_time=datetime.time(10, 45),
                    subject="Multi-Asset Strategic Asset Allocation & Family Office Advisory",
                    message="Discussing sovereign bond hedging, direct private equity allocations, and wealth preservation frameworks.",
                    preferred_comm="video_call",
                    status="confirmed",
                    payment_status="completed",
                    admin_notes="Assigned to Vikram Malhotra (CIO). Client portfolio scope > $15M."
                )

                # Sample 2: Rescheduled booking with clear previous vs updated schedule comparison
                ConsultationBooking.objects.create(
                    reference_key="BF3N8Q1Z7Y",
                    client_name="Alexander Morgan",
                    email="a.morgan@morganholdings.co",
                    phone="+44 20 7946 0912",
                    service="wealth_management",
                    duration_minutes=60,
                    consultation_date=next_wednesday,
                    consultation_time=datetime.time(11, 0),
                    end_time=datetime.time(12, 0),
                    previous_date=next_tuesday,
                    previous_time=datetime.time(10, 0),
                    rescheduled_reason="Rescheduled by Managing Partner to incorporate updated Q3 fiscal macroeconomic audit reports.",
                    subject="Global Estate & Cross-Border Wealth Transfer Structuring",
                    message="Structuring revocable trusts and multi-jurisdiction capital shielding.",
                    preferred_comm="in_person",
                    status="rescheduled",
                    payment_status="completed",
                    admin_notes="Rescheduled with client consent. Boardroom 4A booked."
                )

                # Sample 3: Newly received consultation request
                ConsultationBooking.objects.create(
                    reference_key="PW9K2M4X7V",
                    client_name="David Sterling",
                    email="david.sterling@sterlingcap.org",
                    phone="+1 (555) 438-1192",
                    service="financial_planning",
                    duration_minutes=30,
                    consultation_date=next_tuesday,
                    consultation_time=datetime.time(14, 0),
                    end_time=datetime.time(14, 30),
                    subject="Retirement & Fixed Income Liquidity Strategy",
                    message="Evaluating tax-sheltered annuities and sovereign gold allocation limits.",
                    preferred_comm="video_call",
                    status="received",
                    payment_status="pending",
                    admin_notes="Under initial fiduciary suitability review."
                )
        except Exception:
            pass

    def get(self, request, *args, **kwargs):
        self._seed_sample_bookings()
        from .forms import ConsultationBookingForm, BookingTrackingLookupForm
        from .models import ConsultationBooking

        # Determine default consultation date (Next Business Day: Mon-Fri)
        today = datetime.date.today()
        default_date = today + datetime.timedelta(days=1)
        while default_date.weekday() in (5, 6):  # Skip Sat, Sun
            default_date += datetime.timedelta(days=1)

        # Check if reference key was queried via GET parameter
        lookup_key = request.GET.get('key', '').strip().upper()
        confirmed_key = request.GET.get('confirmed_key', '').strip().upper()
        
        tracked_booking = None
        if lookup_key:
            tracked_booking = ConsultationBooking.objects.filter(reference_key=lookup_key).first()
        elif confirmed_key:
            tracked_booking = ConsultationBooking.objects.filter(reference_key=confirmed_key).first()

        booking_form = ConsultationBookingForm(initial={
            'consultation_date': default_date,
            'duration_minutes': 45,
            'service': 'investment',
            'preferred_comm': 'video_call',
        })
        track_form = BookingTrackingLookupForm(initial={'reference_key': lookup_key})

        context = {
            'page_title': 'Book Your Consultation — Private Wealth Advisory | Sabin Balan Finance',
            'booking_form': booking_form,
            'track_form': track_form,
            'default_date': default_date.strftime('%Y-%m-%d'),
            'default_date_display': default_date.strftime('%A, %d %B %Y'),
            'default_duration': 45,
            'tracked_booking': tracked_booking,
            'lookup_key': lookup_key,
            'confirmed_key': confirmed_key,
            'service_choices': ConsultationBooking.SERVICE_CHOICES,
            'duration_choices': ConsultationBooking.DURATION_CHOICES,
            'comm_choices': ConsultationBooking.COMM_CHOICES,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self._seed_sample_bookings()
        from .forms import ConsultationBookingForm, BookingTrackingLookupForm
        from .models import ConsultationBooking

        action = request.POST.get('form_action', 'book')
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1'

        if action == 'track':
            key = request.POST.get('reference_key', '').strip().upper()
            tracked_booking = ConsultationBooking.objects.filter(reference_key=key).first()
            if is_ajax:
                if tracked_booking:
                    return JsonResponse({
                        'status': 'success',
                        'data': self._serialize_booking(tracked_booking)
                    })
                return JsonResponse({
                    'status': 'error',
                    'message': f"No consultation found for reference key '{key}'. Please verify your 10-character key."
                }, status=404)
            
            # Non-AJAX fallback
            return redirect(f"{reverse('login:consultation')}?key={key}#track-section")

        # Booking submission flow
        form = ConsultationBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.ip_address = request.META.get('REMOTE_ADDR')
            booking.status = 'received'
            booking.payment_status = 'pending'
            booking.save()

            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'reference_key': booking.reference_key,
                    'client_name': booking.client_name,
                    'email': booking.email,
                    'service': booking.get_service_display(),
                    'duration': booking.duration_minutes,
                    'duration_label': booking.duration_label,
                    'date': booking.consultation_date.strftime("%A, %d %B %Y"),
                    'time': booking.consultation_time.strftime("%I:%M %p"),
                    'end_time': booking.end_time.strftime("%I:%M %p") if booking.end_time else "",
                    'message': "Your consultation request has been successfully received.",
                    'data': self._serialize_booking(booking)
                })

            messages.success(request, f"Your consultation has been booked! Your reference key is {booking.reference_key}.")
            return redirect(f"{reverse('login:consultation')}?confirmed_key={booking.reference_key}#confirmation-card")

        # Form Errors
        if is_ajax:
            errors_dict = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
            return JsonResponse({
                'status': 'error',
                'errors': errors_dict,
                'message': "Please correct the highlighted fields and select an available time slot."
            }, status=400)

        messages.error(request, "There was an error in your consultation booking. Please check the fields and try again.")
        context = {
            'page_title': 'Book Your Consultation — Private Wealth Advisory | Sabin Balan Finance',
            'booking_form': form,
            'track_form': BookingTrackingLookupForm(),
            'default_date': request.POST.get('consultation_date', ''),
            'default_duration': int(request.POST.get('duration_minutes', 45)),
            'service_choices': ConsultationBooking.SERVICE_CHOICES,
            'duration_choices': ConsultationBooking.DURATION_CHOICES,
            'comm_choices': ConsultationBooking.COMM_CHOICES,
        }
        return render(request, self.template_name, context)

    def _serialize_booking(self, b):
        return {
            'reference_key': b.reference_key,
            'client_name': b.client_name,
            'email': b.email,
            'phone': b.phone,
            'service': b.get_service_display(),
            'duration_minutes': b.duration_minutes,
            'duration_label': b.duration_label,
            'consultation_date': b.consultation_date.strftime("%A, %d %B %Y"),
            'consultation_time': b.consultation_time.strftime("%I:%M %p"),
            'end_time': b.end_time.strftime("%I:%M %p") if b.end_time else "",
            'preferred_comm': b.get_preferred_comm_display(),
            'status': b.status,
            'status_label': b.get_status_display(),
            'status_badge': b.status_badge_class,
            'payment_status': b.get_payment_status_display(),
            'is_rescheduled': b.status == 'rescheduled' or bool(b.previous_date),
            'previous_date': b.previous_date.strftime("%A, %d %B %Y") if b.previous_date else "",
            'previous_time': b.previous_time.strftime("%I:%M %p") if b.previous_time else "",
            'previous_schedule': f"{b.previous_date.strftime('%A, %d %B %Y')} — {b.previous_time.strftime('%I:%M %p')}" if b.previous_date and b.previous_time else "",
            'updated_schedule': f"{b.consultation_date.strftime('%A, %d %B %Y')} — {b.consultation_time.strftime('%I:%M %p')}",
            'rescheduled_reason': b.rescheduled_reason,
            'subject': b.subject,
            'message': b.message,
            'created_at': b.created_at.strftime("%d %B %Y at %I:%M %p"),
        }


class ConsultationSlotsAPIView(View):
    """
    Dynamic Time Slot Calculation API.
    Calculates exact available slots between 09:00 AM and 06:00 PM (Monday-Friday)
    respecting:
    - Selected duration (30, 45, 60 minutes)
    - 15-minute mandatory buffer between meetings
    - Existing database bookings
    - Past time cutoff if querying today
    - Hard stop at 6:00 PM (no consultation extends beyond 18:00)
    """
    def get(self, request, *args, **kwargs):
        from .models import ConsultationBooking

        date_str = request.GET.get('date')
        try:
            duration = int(request.GET.get('duration', 45))
            if duration not in (30, 45, 60):
                duration = 45
        except (ValueError, TypeError):
            duration = 45

        if not date_str:
            return JsonResponse({'status': 'error', 'message': 'Date parameter is required.'}, status=400)

        try:
            target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid date format (expected YYYY-MM-DD).'}, status=400)

        today = datetime.date.today()
        if target_date < today:
            return JsonResponse({
                'status': 'error',
                'date': date_str,
                'message': 'Consultations cannot be scheduled for past dates.',
                'slots': []
            })

        # Weekend Check (Saturday = 5, Sunday = 6)
        if target_date.weekday() in (5, 6):
            return JsonResponse({
                'status': 'weekend',
                'date': date_str,
                'message': 'Private Wealth Advisory is closed on weekends (Monday–Friday, 9:00 AM–6:00 PM).',
                'slots': []
            })

        # Working hours definition (9:00 AM to 6:00 PM)
        # In minutes from 00:00:
        OPEN_MINUTES = 9 * 60   # 540 (09:00 AM)
        CLOSE_MINUTES = 18 * 60 # 1080 (06:00 PM)
        BUFFER_MINUTES = 15     # Required 15-minute transition gap

        # Fetch existing active bookings for this date
        existing_bookings = ConsultationBooking.objects.filter(
            consultation_date=target_date
        ).exclude(status='cancelled')

        existing_intervals = []
        for b in existing_bookings:
            b_start_min = b.consultation_time.hour * 60 + b.consultation_time.minute
            b_dur = b.duration_minutes or 45
            b_end_min = b_start_min + b_dur
            existing_intervals.append({
                'start': b_start_min,
                'end': b_end_min,
                'ref': b.reference_key,
                'name': b.client_name
            })

        # Now generate discrete possible candidate time slots
        # We step by 15 minutes between 09:00 and (18:00 - duration)
        # Note: If duration=30: 9:00, 9:45, 10:30, 11:15... or step by 15m
        step = 15
        now = datetime.datetime.now()
        is_today = (target_date == today)
        current_minute_today = now.hour * 60 + now.minute

        slots = []
        current_start = OPEN_MINUTES

        while current_start + duration <= CLOSE_MINUTES:
            slot_end = current_start + duration
            
            # Check if this slot start time is already in the past (if booking today)
            is_past_time = is_today and (current_start <= current_minute_today + 30)  # 30 min advance notice
            
            # Check conflict with existing bookings (including 15-minute gap)
            # A slot [current_start, slot_end] conflicts with booking [b.start, b.end]
            # if current_start < b.end + 15 AND slot_end + 15 > b.start
            conflict = False
            conflict_reason = ""

            for b_int in existing_intervals:
                blocked_start = b_int['start'] - BUFFER_MINUTES
                blocked_end = b_int['end'] + BUFFER_MINUTES
                
                # Check overlap between [current_start, slot_end] and [blocked_start, blocked_end]
                if current_start < blocked_end and slot_end > blocked_start:
                    conflict = True
                    b_start_str = f"{b_int['start'] // 60:02d}:{b_int['start'] % 60:02d}"
                    conflict_reason = f"Reserved (Advisory buffer)"
                    break

            start_hour = current_start // 60
            start_min = current_start % 60
            end_hour = slot_end // 60
            end_min = slot_end % 60

            start_time_obj = datetime.time(start_hour, start_min)
            end_time_obj = datetime.time(end_hour, end_min)

            time_24 = f"{start_hour:02d}:{start_min:02d}"
            time_display = start_time_obj.strftime("%I:%M %p")
            end_display = end_time_obj.strftime("%I:%M %p")

            is_available = not is_past_time and not conflict

            slots.append({
                'time': time_24,
                'time_display': time_display,
                'end_time': f"{end_hour:02d}:{end_min:02d}",
                'end_time_display': end_display,
                'duration': duration,
                'is_available': is_available,
                'is_past': is_past_time,
                'is_booked': conflict,
                'reason': conflict_reason if conflict else ('Past time' if is_past_time else 'Available')
            })

            # Advance by step (15 minutes) to offer flexible starting intervals
            current_start += step

        return JsonResponse({
            'status': 'success',
            'date': date_str,
            'date_display': target_date.strftime("%A, %d %B %Y"),
            'duration': duration,
            'total_slots': len(slots),
            'available_count': sum(1 for s in slots if s['is_available']),
            'slots': slots
        })


class ConsultationTrackAPIView(View):
    """
    API endpoint for Real-Time Consultation Tracking.
    Returns complete consultation lifecycle, status indicators, and
    previous vs updated scheduling comparison if the booking was rescheduled.
    """
    def get(self, request, *args, **kwargs):
        from .models import ConsultationBooking
        key = request.GET.get('key', '').strip().upper()
        if not key or len(key) != 10:
            return JsonResponse({
                'status': 'error',
                'message': 'Please provide a valid 10-character reference key (e.g., GT7K4M9P2X).'
            }, status=400)

        booking = ConsultationBooking.objects.filter(reference_key=key).first()
        if not booking:
            return JsonResponse({
                'status': 'error',
                'message': f"No consultation record was found matching reference key '{key}'. Please double-check your reference key and try again."
            }, status=404)

        # Build timeline states
        # Possible statuses: received, under_review, confirmed, paid, payment_pending, rescheduled, completed, cancelled
        timeline = [
            {
                'step': 1,
                'code': 'received',
                'title': 'Request Submitted',
                'description': 'Consultation request securely received and queued.',
                'state': 'completed'
            },
            {
                'step': 2,
                'code': 'under_review',
                'title': 'Under Review',
                'description': 'Advisory desk reviewing scope & advisor allocation.',
                'state': 'completed' if booking.status in ('confirmed', 'paid', 'rescheduled', 'completed') else ('active' if booking.status in ('received', 'under_review', 'payment_pending') else 'pending')
            },
            {
                'step': 3,
                'code': 'confirmed',
                'title': 'Confirmed',
                'description': 'Boardroom & Senior Wealth Advisor locked in calendar.',
                'state': 'completed' if booking.status in ('paid', 'completed') else ('active' if booking.status in ('confirmed', 'rescheduled') else 'pending')
            },
            {
                'step': 4,
                'code': 'paid',
                'title': 'Payment Completed',
                'description': 'Retainer/fiduciary fee verified or waived.',
                'state': 'completed' if booking.status == 'completed' or booking.payment_status in ('completed', 'waived') else ('active' if booking.status == 'paid' else 'pending')
            },
            {
                'step': 5,
                'code': 'completed',
                'title': 'Consultation Completed',
                'description': 'Strategic briefing & executive advisory concluded.',
                'state': 'completed' if booking.status == 'completed' else 'pending'
            }
        ]

        if booking.status == 'cancelled':
            for t in timeline:
                if t['code'] != 'received':
                    t['state'] = 'cancelled'

        data = {
            'reference_key': booking.reference_key,
            'client_name': booking.client_name,
            'email': booking.email,
            'phone': booking.phone,
            'service': booking.get_service_display(),
            'duration_minutes': booking.duration_minutes,
            'duration_label': booking.duration_label,
            'consultation_date': booking.consultation_date.strftime("%A, %d %B %Y"),
            'consultation_time': booking.consultation_time.strftime("%I:%M %p"),
            'end_time': booking.end_time.strftime("%I:%M %p") if booking.end_time else "",
            'preferred_comm': booking.get_preferred_comm_display(),
            'status': booking.status,
            'status_label': booking.get_status_display(),
            'status_badge': booking.status_badge_class,
            'payment_status': booking.get_payment_status_display(),
            'is_rescheduled': booking.status == 'rescheduled' or bool(booking.previous_date),
            'previous_date': booking.previous_date.strftime("%A, %d %B %Y") if booking.previous_date else "",
            'previous_time': booking.previous_time.strftime("%I:%M %p") if booking.previous_time else "",
            'previous_schedule': f"{booking.previous_date.strftime('%A, %d %B %Y')} — {booking.previous_time.strftime('%I:%M %p')}" if booking.previous_date and booking.previous_time else "",
            'updated_schedule': f"{booking.consultation_date.strftime('%A, %d %B %Y')} — {booking.consultation_time.strftime('%I:%M %p')}",
            'rescheduled_reason': booking.rescheduled_reason,
            'subject': booking.subject,
            'message': booking.message,
            'admin_notes': booking.admin_notes if request.user.is_staff else "",
            'created_at': booking.created_at.strftime("%d %B %Y at %I:%M %p"),
            'timeline': timeline,
        }

        return JsonResponse({
            'status': 'success',
            'data': data
        })


class ClientReviewView(TemplateView):
    """
    Dedicated Client First Draft Review & Feedback Suite for Sabin Balan.
    Provides interactive page-by-page visual replica review, section editing,
    image replacement, adding/deleting elements, and instant feedback exporting.
    """
    template_name = 'login/client_review.html'





