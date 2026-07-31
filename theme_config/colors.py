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
# NAMED COLOR CONSTANTS (Palette Color Definitions)
# ============================================================

DEEP_ROYAL_PURPLE = "#000000" # Primary headings & text (Deep Royal Purple)
WARM_PEACH_CREAM = "#FFF7ED"        # Containers & Cards background (Warm Peach Cream)
SOFT_LAVENDER = "#F5F3FF"           # Page Body Background (Soft Lavender)
COOL_SLATE_GRAY = "#6B7280"         # Subtext, labels & secondary text (Cool Slate Gray)
SOFT_LAVENDER_BORDER = "#DDD6FE"    # Soft Lavender Border
VIBRANT_VIOLET = "#6D28D9"          # Primary hover state (Vibrant Violet)
ULTRA_SOFT_PURPLE = "#FAF5FF"      # Form input fields background (Ultra Soft Purple)
FOREST_GREEN = "#15803D"            # Success notification text (Forest Green)
SOFT_MINT = "#F0FDF4"               # Success alert pill background (Soft Mint)
DEEP_CRIMSON = "#B91C1C"            # Error alert text (Deep Crimson)
SOFT_ROSE = "#FEF2F2"              # Error alert pill background (Soft Rose)
GOLDEN_AMBER = "#F59E0B"          # Golden Amber Accent
BRIGHT_CYAN = "#06B6D4"           # Bright Cyan Blue

# Dark Theme Named Color Constants
CRISP_SILVER_WHITE = "#F8FAFC"      # Primary text & CTA (Crisp Silver-White)
DEEP_OBSIDIAN_NAVY = "#0F172A"      # Card & Surface background (Deep Obsidian Navy)
MIDNIGHT_ONYX = "#06080D"           # Page Background (Ultra-Deep Midnight Onyx)
MUTED_SILVER_GREY = "#94A3B8"     # Subtext (Muted Silver-Grey)
SUBTLE_GLASS_BORDER = "rgba(255, 255, 255, 0.1)" # Subtle glass border
LIGHT_CTA_HOVER = "#E2E8F0"        # CTA hover
DARK_INPUT_BG = "#1E293B"         # Input fields background
EMERALD_GREEN = "#34D399"         # Success text (Emerald Green)
EMERALD_PILL_BG = "rgba(16, 185, 129, 0.15)" # Success pill bg
BRIGHT_RED = "#F87171"            # Error text
RED_PILL_BG = "rgba(239, 68, 68, 0.15)" # Error pill bg
GOLD_ACCENT_GLOW = "#F5D77F"      # Gold accent glow
CYAN_GLOW = "#00F2FE"            # Cyan glow accent


# ============================================================
# LIGHT THEME PALETTE ASSIGNMENTS
# ============================================================

COLOR_PRIMARY = DEEP_ROYAL_PURPLE
COLOR_SECONDARY = WARM_PEACH_CREAM
COLOR_BG = SOFT_LAVENDER
COLOR_TEXT_SUB = COOL_SLATE_GRAY
COLOR_BORDER = SOFT_LAVENDER_BORDER
COLOR_PRIMARY_HOVER = VIBRANT_VIOLET
COLOR_INPUT_BG = ULTRA_SOFT_PURPLE
COLOR_SUCCESS = FOREST_GREEN
COLOR_SUCCESS_BG = SOFT_MINT
COLOR_ERROR = DEEP_CRIMSON
COLOR_ERROR_BG = SOFT_ROSE
COLOR_GOLD = GOLDEN_AMBER
COLOR_CYAN = BRIGHT_CYAN


# ============================================================
# DARK THEME PALETTE ASSIGNMENTS
# ============================================================

DARK_COLOR_PRIMARY = CRISP_SILVER_WHITE
DARK_COLOR_SECONDARY = DEEP_OBSIDIAN_NAVY
DARK_COLOR_BG = MIDNIGHT_ONYX
DARK_COLOR_TEXT_SUB = MUTED_SILVER_GREY
DARK_COLOR_BORDER = SUBTLE_GLASS_BORDER
DARK_COLOR_PRIMARY_HOVER = LIGHT_CTA_HOVER
DARK_COLOR_INPUT_BG = DARK_INPUT_BG
DARK_COLOR_SUCCESS = EMERALD_GREEN
DARK_COLOR_SUCCESS_BG = EMERALD_PILL_BG
DARK_COLOR_ERROR = BRIGHT_RED
DARK_COLOR_ERROR_BG = RED_PILL_BG
DARK_COLOR_GOLD = GOLD_ACCENT_GLOW
DARK_COLOR_CYAN = CYAN_GLOW


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
        f"--color-success-border: rgba(21, 128, 61, 0.25);",
        f"--color-error: {COLOR_ERROR};",
        f"--color-error-bg: {COLOR_ERROR_BG};",
        f"--color-error-border: rgba(185, 28, 28, 0.25);",
        f"--color-info: {COLOR_CYAN};",
        f"--color-info-bg: #ECFEFF;",
        f"--color-info-border: rgba(6, 182, 212, 0.2);",
        f"--color-focus-ring: rgba(59, 7, 100, 0.2);",
        f"--color-avatar-shadow: rgba(59, 7, 100, 0.12);",
        f"--color-gold: {COLOR_GOLD};",
        f"--color-cyan: {COLOR_CYAN};",
        f"--color-glass-bg: rgba(255, 247, 237, 0.92);",
        f"--color-glass-border: rgba(221, 214, 254, 0.5);",
        f"--color-body-gradient: {COLOR_BG};",
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
        f"--color-body-gradient: radial-gradient(circle at 50% 20%, rgba(212, 175, 55, 0.15) 0%, rgba(6, 8, 13, 0.95) 70%), linear-gradient(180deg, #0A0D14 0%, #06080D 100%);",
    ]

    light_str = "\n  ".join(light_vars)
    dark_str = "\n  ".join(dark_vars)

    return f":root {{\n  {light_str}\n}}\n\n[data-theme='dark'] {{\n  {dark_str}\n}}"
