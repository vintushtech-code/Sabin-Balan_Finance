"""
Central Color Palette Configuration Module — Jio BlackRock Executive Styling
=============================================================================

This file centralizes all theme colors for the entire application.
Changing a single variable or palette value here updates the UI globally
across all apps (login, landing, navigation, buttons, cards, inputs).

The colors are exposed via context processor to CSS custom properties (--color-*).
Supports both Light Theme and Dark Theme (activated via data-theme="dark" on <html>).
"""

# ============================================================
# LIGHT THEME PALETTE (Executive Crisp Slate)
# ============================================================

COLOR_PRIMARY = "#0F172A"        # Primary headings & text (Rich Obsidian Slate)
COLOR_SECONDARY = "#FFFFFF"      # Containers, Cards background (Clean White)
COLOR_BG = "#F8FAFC"             # Page Body Background (Porcelain Slate White)
COLOR_TEXT_SUB = "#475569"       # Subtext, labels, placeholder & secondary text
COLOR_BORDER = "#E2E8F0"         # Clean corporate border line
COLOR_PRIMARY_HOVER = "#1E293B" # Button hover state
COLOR_INPUT_BG = "#F1F5F9"       # Form input fields background
COLOR_SUCCESS = "#059669"        # Success notification text (Emerald Green)
COLOR_SUCCESS_BG = "#ECFDF5"     # Success alert pill background
COLOR_ERROR = "#DC2626"          # Error alert text
COLOR_ERROR_BG = "#FEF2F2"       # Error alert pill background
COLOR_GOLD = "#D4AF37"           # Metallic Gold Accent
COLOR_CYAN = "#0284C7"           # Corporate Cyan Blue

# ============================================================
# DARK THEME PALETTE (Jio BlackRock Midnight Onyx & Gold)
# ============================================================

DARK_COLOR_PRIMARY = "#F8FAFC"       # Primary text & CTA (Crisp Silver-White)
DARK_COLOR_SECONDARY = "#0F172A"     # Card & Surface background (Deep Obsidian Navy)
DARK_COLOR_BG = "#06080D"            # Page Background (Ultra-Deep Midnight Onyx)
DARK_COLOR_TEXT_SUB = "#94A3B8"      # Subtext (Muted Silver-Grey)
DARK_COLOR_BORDER = "rgba(255, 255, 255, 0.1)" # Subtle glass border
DARK_COLOR_PRIMARY_HOVER = "#E2E8F0" # CTA hover
DARK_COLOR_INPUT_BG = "#1E293B"      # Input fields background
DARK_COLOR_SUCCESS = "#34D399"       # Success text (Emerald Green)
DARK_COLOR_SUCCESS_BG = "rgba(16, 185, 129, 0.15)" # Success pill bg
DARK_COLOR_ERROR = "#F87171"         # Error text
DARK_COLOR_ERROR_BG = "rgba(239, 68, 68, 0.15)" # Error pill bg
DARK_COLOR_GOLD = "#F5D77F"         # Gold accent glow
DARK_COLOR_CYAN = "#00F2FE"         # Cyan glow accent


THEME_PALETTE = {
    # Light
    "COLOR_PRIMARY": COLOR_PRIMARY,
    "COLOR_SECONDARY": COLOR_SECONDARY,
    "COLOR_BG": COLOR_BG,
    "COLOR_TEXT_SUB": COLOR_TEXT_SUB,
    "COLOR_BORDER": COLOR_BORDER,
    "COLOR_PRIMARY_HOVER": COLOR_PRIMARY_HOVER,
    "COLOR_INPUT_BG": COLOR_INPUT_BG,
    "COLOR_SUCCESS": COLOR_SUCCESS,
    "COLOR_SUCCESS_BG": COLOR_SUCCESS_BG,
    "COLOR_ERROR": COLOR_ERROR,
    "COLOR_ERROR_BG": COLOR_ERROR_BG,
    "COLOR_GOLD": COLOR_GOLD,
    "COLOR_CYAN": COLOR_CYAN,
    # Dark
    "DARK_COLOR_PRIMARY": DARK_COLOR_PRIMARY,
    "DARK_COLOR_SECONDARY": DARK_COLOR_SECONDARY,
    "DARK_COLOR_BG": DARK_COLOR_BG,
    "DARK_COLOR_TEXT_SUB": DARK_COLOR_TEXT_SUB,
    "DARK_COLOR_BORDER": DARK_COLOR_BORDER,
    "DARK_COLOR_PRIMARY_HOVER": DARK_COLOR_PRIMARY_HOVER,
    "DARK_COLOR_INPUT_BG": DARK_COLOR_INPUT_BG,
    "DARK_COLOR_SUCCESS": DARK_COLOR_SUCCESS,
    "DARK_COLOR_SUCCESS_BG": DARK_COLOR_SUCCESS_BG,
    "DARK_COLOR_ERROR": DARK_COLOR_ERROR,
    "DARK_COLOR_ERROR_BG": DARK_COLOR_ERROR_BG,
    "DARK_COLOR_GOLD": DARK_COLOR_GOLD,
    "DARK_COLOR_CYAN": DARK_COLOR_CYAN,
}


def get_css_variables():
    """
    Generates CSS custom property declarations for both light and dark themes.
    """
    light_vars = [
        f"--color-primary: {COLOR_PRIMARY};",
        f"--color-secondary: {COLOR_SECONDARY};",
        f"--color-bg: {COLOR_BG};",
        f"--color-subtext: {COLOR_TEXT_SUB};",
        f"--color-border: {COLOR_BORDER};",
        f"--color-primary-hover: {COLOR_PRIMARY_HOVER};",
        f"--color-input-bg: {COLOR_INPUT_BG};",
        f"--color-success: {COLOR_SUCCESS};",
        f"--color-success-bg: {COLOR_SUCCESS_BG};",
        f"--color-success-border: rgba(5, 150, 105, 0.25);",
        f"--color-error: {COLOR_ERROR};",
        f"--color-error-bg: {COLOR_ERROR_BG};",
        f"--color-error-border: rgba(220, 38, 38, 0.25);",
        f"--color-info: #0284c7;",
        f"--color-info-bg: #e0f2fe;",
        f"--color-info-border: rgba(2, 132, 199, 0.2);",
        f"--color-focus-ring: rgba(15, 23, 42, 0.1);",
        f"--color-avatar-shadow: rgba(0, 0, 0, 0.12);",
        f"--color-gold: {COLOR_GOLD};",
        f"--color-cyan: {COLOR_CYAN};",
        f"--color-glass-bg: rgba(255, 255, 255, 0.85);",
        f"--color-glass-border: rgba(15, 23, 42, 0.08);",
    ]

    dark_vars = [
        f"--color-primary: {DARK_COLOR_PRIMARY};",
        f"--color-secondary: {DARK_COLOR_SECONDARY};",
        f"--color-bg: {DARK_COLOR_BG};",
        f"--color-subtext: {DARK_COLOR_TEXT_SUB};",
        f"--color-border: {DARK_COLOR_BORDER};",
        f"--color-primary-hover: {DARK_COLOR_PRIMARY_HOVER};",
        f"--color-input-bg: {DARK_COLOR_INPUT_BG};",
        f"--color-success: {DARK_COLOR_SUCCESS};",
        f"--color-success-bg: {DARK_COLOR_SUCCESS_BG};",
        f"--color-success-border: rgba(52, 211, 153, 0.25);",
        f"--color-error: {DARK_COLOR_ERROR};",
        f"--color-error-bg: {DARK_COLOR_ERROR_BG};",
        f"--color-error-border: rgba(248, 113, 113, 0.25);",
        f"--color-info: #38bdf8;",
        f"--color-info-bg: rgba(56, 189, 248, 0.15);",
        f"--color-info-border: rgba(56, 189, 248, 0.25);",
        f"--color-focus-ring: rgba(248, 250, 252, 0.12);",
        f"--color-avatar-shadow: rgba(0, 0, 0, 0.4);",
        f"--color-gold: {DARK_COLOR_GOLD};",
        f"--color-cyan: {DARK_COLOR_CYAN};",
        f"--color-glass-bg: rgba(15, 23, 42, 0.75);",
        f"--color-glass-border: rgba(255, 255, 255, 0.12);",
    ]

    light_str = "\n  ".join(light_vars)
    dark_str = "\n  ".join(dark_vars)

    return f":root {{\n  {light_str}\n}}\n\n[data-theme='dark'] {{\n  {dark_str}\n}}"
