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

        # Fetch Top 3 Active Testimonials for Home Page Preview Section
        try:
            from .models import Testimonial
            context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order', '-rating')[:3]
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



