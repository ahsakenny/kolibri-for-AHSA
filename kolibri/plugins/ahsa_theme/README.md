# AHSA Learning Network - Theme Plugin Documentation

## Overview

The AHSA Theme Plugin provides white-label branding for transforming Kolibri into the AHSA Learning Network platform. This plugin follows Kolibri's established plugin architecture to provide maintainable, upgradeable branding customization.

## Features

- Custom logo and favicon support
- Configurable color scheme (primary and secondary colors)
- Custom login page branding
- Custom browser tab titles
- Configurable footer text
- Environment variable or config file based configuration

## Installation & Activation

### 1. Enable the Plugin

```bash
kolibri plugin enable kolibri.plugins.ahsa_theme
kolibri plugin disable kolibri.plugins.default_theme  # Disable default theme
```

### 2. Restart Kolibri

```bash
kolibri stop
kolibri start
```

## Configuration

### Environment Variables

Set these environment variables before starting Kolibri:

```bash
export AHSA_BRAND_NAME="AHSA Learning Network"
export AHSA_PRIMARY_COLOR="#003366"        # Navy blue
export AHSA_SECONDARY_COLOR="#FFA500"      # Orange
export AHSA_LOGIN_WELCOME_TEXT="Welcome to AHSA Learning Network"
export AHSA_FOOTER_TEXT="© American High School Academy - AHSA Learning Network"
export AHSA_ENABLE_BRANDING=true
```

### Configuration File (options.ini)

Alternatively, add these settings to `$KOLIBRI_HOME/options.ini`:

```ini
[Branding]
AHSA_BRAND_NAME = AHSA Learning Network
AHSA_PRIMARY_COLOR = #003366
AHSA_SECONDARY_COLOR = #FFA500
AHSA_LOGIN_WELCOME_TEXT = Welcome to AHSA Learning Network
AHSA_FOOTER_TEXT = © American High School Academy - AHSA Learning Network
AHSA_ENABLE_BRANDING = true
```

## Branding Assets

### Required Files

Replace the placeholder files in `static/assets/ahsa_theme/` with actual AHSA branding:

1. **ahsa-logo.svg** - Main scalable logo (SVG format)
2. **ahsa-logo-192.png** - App icon (192x192 pixels, PNG)
3. **ahsa-logo-512.png** - App icon (512x512 pixels, PNG)
4. **ahsa-favicon.ico** - Browser favicon (32x32 pixels, ICO format)
5. **ahsa-background.jpg** - Login page background (1920x1080 recommended, JPG)

### Asset Guidelines

- **Colors**: Primary Navy Blue (#003366), Secondary Orange (#FFA500)
- **Logo**: Should work on both light and dark backgrounds
- **Background**: High quality, appropriate for educational context
- **Optimization**: Compress images for web use
- **Attribution**: Ensure all images are properly licensed

## Architecture

### Plugin Structure

```
kolibri/plugins/ahsa_theme/
├── __init__.py              # Plugin initialization
├── apps.py                  # Django app configuration
├── kolibri_plugin.py        # Main plugin with ThemeHook
├── options.py               # Configuration options specification
└── static/
    └── assets/
        └── ahsa_theme/
            ├── README.md    # Asset documentation
            ├── ahsa-logo.svg
            ├── ahsa-logo-192.png
            ├── ahsa-logo-512.png
            ├── ahsa-favicon.ico
            └── ahsa-background.jpg
```

### How It Works

1. The plugin extends `KolibriPluginBase` and registers a `ThemeHook`
2. The ThemeHook overrides default Kolibri theming
3. Configuration is loaded from environment variables or options.ini
4. Static assets are served via Django's static file system
5. Theme applies to all user-facing pages

## Customization

### Changing Colors

The theme supports dynamic color customization:

```python
# In options.ini or environment variables
AHSA_PRIMARY_COLOR = #1a5490     # Different shade of blue
AHSA_SECONDARY_COLOR = #ff8c00   # Different shade of orange
```

Colors are automatically applied to:
- Top navigation bar
- Side navigation
- Buttons and links
- Login page accents

### Adding Custom CSS

For advanced styling beyond color changes, you can:

1. Create a custom CSS file in `static/assets/ahsa_theme/custom.css`
2. Override specific Kolibri Design System tokens
3. Use the `tokenMapping` in the theme configuration

## String Replacement Strategy

### User-Facing Strings

While the theme plugin handles visual branding, user-facing text strings are handled separately through Kolibri's internationalization system. Key strings to customize:

- Application name (via theme config)
- Login welcome message (via theme config)
- Footer text (via theme config)

For complete string replacement ("Kolibri" → "AHSA Learning Network"), see the separate i18n customization guide.

## Troubleshooting

### Theme Not Applying

1. Verify plugin is enabled: `kolibri plugin list`
2. Ensure default_theme is disabled
3. Check options.ini for correct syntax
4. Clear browser cache
5. Restart Kolibri server

### Logo Not Showing

1. Verify files exist in `static/assets/ahsa_theme/`
2. Check file permissions (must be readable)
3. Run `kolibri manage collectstatic`
4. Clear browser cache

### Colors Not Changing

1. Verify hex color format (#RRGGBB)
2. Check options.ini or environment variables
3. Restart Kolibri after configuration changes
4. Clear browser cache and hard refresh

## Maintenance

### Upgrading Kolibri

This plugin is designed to be upgrade-safe:

1. Plugin code doesn't modify Kolibri core
2. Uses stable Kolibri APIs (ThemeHook)
3. Configuration is external (options.ini)
4. Assets are in plugin directory

Before upgrading Kolibri:
1. Backup your configuration
2. Backup your custom assets
3. Test in a staging environment
4. Review Kolibri changelog for theme API changes

### Backing Up Configuration

```bash
# Backup options.ini
cp $KOLIBRI_HOME/options.ini $KOLIBRI_HOME/options.ini.backup

# Backup custom assets
tar -czf ahsa-assets-backup.tar.gz kolibri/plugins/ahsa_theme/static/
```

## Support & Contribution

For issues or enhancements:

1. Check the main AHSA customization documentation
2. Review Kolibri's theme documentation
3. Contact your Kolibri administrator

## License & Attribution

This plugin extends Kolibri, which is licensed under the MIT License.
The plugin itself maintains the same license.

All AHSA branding assets are property of American High School Academy.

Kolibri attribution is maintained in the codebase and documentation as required by the license.

## See Also

- Kolibri Theme Hook Documentation: `kolibri/core/theme_hook.py`
- Default Theme Plugin: `kolibri/plugins/default_theme/`
- Kolibri Plugin Architecture: `docs/backend_architecture/plugins.rst`
- AHSA Courses Plugin: `kolibri/plugins/ahsa_courses/` (for course content customization)
