"""
AHSA Learning Network Theme Plugin
==================================

This plugin implements white-label branding for the American High School Academy (AHSA)
Learning Network using Kolibri's ThemeHook system.
"""
from django.templatetags.static import static

from kolibri.core import theme_hook
from kolibri.plugins import KolibriPluginBase
from kolibri.plugins.hooks import register_hook
from kolibri.utils import conf


class AHSAThemePlugin(KolibriPluginBase):
    """
    Main plugin class for AHSA theme.
    Registers options for branding configuration.
    """

    # Reference to the options module for configuration
    options = "options"


@register_hook
class AHSAThemeHook(theme_hook.ThemeHook):
    """
    Custom theme hook for AHSA Learning Network branding.

    This hook overrides default Kolibri branding with AHSA-specific:
    - Logos and favicons
    - Color scheme
    - Login page customization
    - Sign-in background
    """

    @property
    def theme(self):
        """
        Define the AHSA theme configuration.

        Returns theme dictionary with:
        - signIn: Login page customization
        - logos: Icon and logo variants
        - tokenMapping: Color overrides (optional)
        """
        # Get configuration from OPTIONS
        brand_name = conf.OPTIONS["Branding"]["AHSA_BRAND_NAME"]
        primary_color = conf.OPTIONS["Branding"]["AHSA_PRIMARY_COLOR"]
        secondary_color = conf.OPTIONS["Branding"]["AHSA_SECONDARY_COLOR"]
        login_text = conf.OPTIONS["Branding"]["AHSA_LOGIN_WELCOME_TEXT"]

        theme_config = {
            "signIn": {
                # Use AHSA background image for sign-in page
                "background": static("assets/ahsa_theme/ahsa-background.jpg"),
                "backgroundImgCredit": "American High School Academy",
                "topLogo": {
                    "style": "padding-left: 64px; padding-right: 64px; margin-bottom: 8px; margin-top: 8px",
                },
                # Custom sign-in page title (if supported by frontend)
                "title": login_text,
            },
            "logos": [
                {
                    "src": static("assets/ahsa_theme/ahsa-favicon.ico"),
                    "content_type": "image/vnd.microsoft.icon",
                    "size": "32x32",
                },
                {
                    "src": static("assets/ahsa_theme/ahsa-logo.svg"),
                    "content_type": "image/svg+xml",
                    "maskable": True,
                    "size": "any",
                },
                {
                    "src": static("assets/ahsa_theme/ahsa-logo-192.png"),
                    "content_type": "image/png",
                    "size": "192x192",
                },
                {
                    "src": static("assets/ahsa_theme/ahsa-logo-512.png"),
                    "content_type": "image/png",
                    "size": "512x512",
                },
            ],
            # Token mapping for color overrides
            # This allows customization of Kolibri's theme tokens
            "tokenMapping": {
                "primary": primary_color,
                "primaryDark": self._darken_color(primary_color),
                "secondary": secondary_color,
            },
            "sideNav": {
                "backgroundColor": primary_color,
            },
            "appBar": {
                "backgroundColor": primary_color,
            },
        }

        return theme_config

    def _darken_color(self, color_hex, factor=0.8):
        """
        Darken a hex color by a factor.

        Args:
            color_hex (str): Hex color string (e.g., "#003366")
            factor (float): Darkening factor (0.0 to 1.0)

        Returns:
            str: Darkened hex color
        """
        # Remove '#' if present
        color_hex = color_hex.lstrip("#")

        # Convert hex to RGB
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)

        # Darken
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        # Convert back to hex
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
