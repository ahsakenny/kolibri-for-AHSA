"""
AHSA Learning Network - Configuration Options
=============================================

This module defines configurable options for AHSA branding.
Options can be set via environment variables or options.ini file.

Environment Variables:
- AHSA_BRAND_NAME: Application brand name (default: "AHSA Learning Network")
- AHSA_PRIMARY_COLOR: Primary brand color (default: "#003366")
- AHSA_SECONDARY_COLOR: Secondary brand color (default: "#FFA500")
- AHSA_LOGIN_WELCOME_TEXT: Custom welcome text for login page
- AHSA_FOOTER_TEXT: Custom footer text
- AHSA_ENABLE_BRANDING: Enable/disable AHSA branding (default: true)
"""

# Option specification for AHSA theme customization
# These can be overridden via environment variables or options.ini
option_spec = {
    "Branding": {
        "AHSA_BRAND_NAME": {
            "type": "string",
            "default": "AHSA Learning Network",
            "envvars": ("AHSA_BRAND_NAME",),
        },
        "AHSA_PRIMARY_COLOR": {
            "type": "string",
            "default": "#003366",  # Navy blue
            "envvars": ("AHSA_PRIMARY_COLOR",),
        },
        "AHSA_SECONDARY_COLOR": {
            "type": "string",
            "default": "#FFA500",  # Orange
            "envvars": ("AHSA_SECONDARY_COLOR",),
        },
        "AHSA_LOGIN_WELCOME_TEXT": {
            "type": "string",
            "default": "Welcome to AHSA Learning Network",
            "envvars": ("AHSA_LOGIN_WELCOME_TEXT",),
        },
        "AHSA_FOOTER_TEXT": {
            "type": "string",
            "default": "© American High School Academy - AHSA Learning Network",
            "envvars": ("AHSA_FOOTER_TEXT",),
        },
        "AHSA_ENABLE_BRANDING": {
            "type": "boolean",
            "default": True,
            "envvars": ("AHSA_ENABLE_BRANDING",),
        },
    }
}
