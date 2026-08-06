import re

with open(r'c:\Users\USER\Desktop\finance_website\Sabin-Balan_Finance\service section\styles.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

with open(r'c:\Users\USER\Desktop\finance_website\Sabin-Balan_Finance\service section\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
body_inner = body_match.group(1)

# Remove standalone header
body_inner = re.sub(r'<!-- Header -->.*?</header>', '', body_inner, flags=re.DOTALL)
# Remove standalone footer
body_inner = re.sub(r'<!-- Footer Section -->.*?</footer>', '', body_inner, flags=re.DOTALL)

# Replace image asset paths with Django static tag using lambda function
body_inner = re.sub(r'src=["\']assets/([^"\']+)["\']', lambda m: f'src="{{% static \'login/images/{m.group(1)}\' %}}"', body_inner)
# Replace video asset paths with Django static tag
body_inner = re.sub(r'src=["\'](?:\.\./)?videos/([^"\']+)["\']', lambda m: f'src="{{% static \'{m.group(1)}\' %}}"', body_inner)
# Replace poster paths with Django static tag
body_inner = re.sub(r'poster=["\']assets/([^"\']+)["\']', lambda m: f'poster="{{% static \'login/images/{m.group(1)}\' %}}"', body_inner)

final_template = f"""{{% extends 'theme_config/base.html' %}}
{{% load static %}}

{{% block title %}}Sabin Balan Finance — Wealth & Institutional Advisory Services{{% endblock %}}

{{% block extra_css %}}
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{css_content}
</style>
{{% endblock %}}

{{% block content %}}
{body_inner}
{{% endblock %}}
"""

with open(r'c:\Users\USER\Desktop\finance_website\Sabin-Balan_Finance\login\templates\login\services.html', 'w', encoding='utf-8') as f:
    f.write(final_template)

print("Regenerated services.html cleanly with lambda repls!")
