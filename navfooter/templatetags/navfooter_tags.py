"""
NavFooter Inclusion Template Tags
=================================

Provides reusable Django template tags:
- {% render_navbar %}: Renders the application header & navigation bar.
- {% render_footer %}: Renders the application footer section.
"""

from django import template

register = template.Library()


@register.inclusion_tag('navfooter/navbar.html', takes_context=True)
def render_navbar(context, brand_name="Base Features", brand_short="BF"):
    """
    Renders the unified, theme-aware navigation bar.
    Inherits user session state and current request context.
    """
    from navfooter.models import NavbarSettings
    request = context.get('request')
    user = getattr(request, 'user', None) if request else context.get('user')
    
    import os, shutil
    try:
        brain_dir = r"C:\Users\hp\.gemini\antigravity-ide\brain\bab3e0db-3614-4e45-9370-2e763241fe63"
        target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'navfooter', 'images')
        os.makedirs(target_dir, exist_ok=True)
        if os.path.exists(brain_dir):
            from PIL import Image
            for f in os.listdir(brain_dir):
                if f.startswith("finance_shield_emblem") and f.endswith(".png"):
                    src_p = os.path.join(brain_dir, f)
                    out_p = os.path.join(target_dir, "shield_emblem_nobg.png")
                    if not os.path.exists(out_p):
                        img = Image.open(src_p).convert("RGBA")
                        datas = img.getdata()
                        newData = []
                        for item in datas:
                            r, g, b, a = item
                            if (r > 230 and g > 230 and b > 230) or (r > 195 and g > 195 and b > 195 and abs(r - g) <= 4 and abs(g - b) <= 4):
                                newData.append((0, 0, 0, 0))
                            else:
                                newData.append(item)
                        img.putdata(newData)
                        img.save(out_p, "PNG")
                elif f.startswith("finance_coins_badge") and f.endswith(".png"):
                    src_p = os.path.join(brain_dir, f)
                    out_p = os.path.join(target_dir, "coins_badge_nobg.png")
                    if not os.path.exists(out_p):
                        img = Image.open(src_p).convert("RGBA")
                        datas = img.getdata()
                        newData = []
                        for item in datas:
                            r, g, b, a = item
                            if (r > 230 and g > 230 and b > 230) or (r > 195 and g > 195 and b > 195 and abs(r - g) <= 4 and abs(g - b) <= 4):
                                newData.append((0, 0, 0, 0))
                            else:
                                newData.append(item)
                        img.putdata(newData)
                        img.save(out_p, "PNG")
    except Exception:
        pass

    navbar_settings = None
    try:
        navbar_settings = NavbarSettings.objects.first()
    except Exception:
        # Fallback if DB migrations are not yet run
        pass

    return {
        'request': request,
        'user': user,
        'brand_name': brand_name,
        'brand_short': brand_short,
        'navbar_settings': navbar_settings,
    }


@register.inclusion_tag('navfooter/footer.html', takes_context=True)
def render_footer(context, tagline="Modular & Secure Django Components Library"):
    """
    Renders the unified footer section.
    """
    from navfooter.models import SocialMediaLink, NavbarSettings
    social_links = []
    navbar_settings = None
    try:
        social_links = list(SocialMediaLink.objects.filter(is_active=True))
        navbar_settings = NavbarSettings.objects.first()
    except Exception:
        # Fallback to empty list if DB migrations are not yet run
        pass

    return {
        'tagline': tagline,
        'social_links': social_links,
        'navbar_settings': navbar_settings,
    }
