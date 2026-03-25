# AHSA Learning Network - Complete Setup Guide

This guide provides complete instructions for deploying and configuring the AHSA Learning Network white-label transformation of Kolibri.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Branding Setup](#branding-setup)
5. [Course Seeding](#course-seeding)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)
8. [Upgrading Kolibri](#upgrading-kolibri)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.6+ installed
- pip and virtualenv
- Node.js 14+ and pnpm (for development)
- Git
- Sufficient disk space (5GB+ recommended)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/ahsakenny/kolibri-for-AHSA.git
cd kolibri-for-AHSA
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements/dev.txt
pnpm install  # If doing development work
```

### 4. Set Environment Variables

```bash
export KOLIBRI_HOME=$HOME/.kolibri-ahsa  # Custom data directory
export KOLIBRI_RUN_MODE=dev  # Or 'production'
```

### 5. Initialize Kolibri

```bash
kolibri configure setup
```

This creates the database and runs initial migrations.

## Configuration

### 1. Enable AHSA Plugins

```bash
# Disable default theme
kolibri plugin disable kolibri.plugins.default_theme

# Enable AHSA plugins
kolibri plugin enable kolibri.plugins.ahsa_theme
kolibri plugin enable kolibri.plugins.ahsa_courses
```

### 2. Configure Branding

Create or edit `$KOLIBRI_HOME/options.ini`:

```ini
[Branding]
AHSA_BRAND_NAME = AHSA Learning Network
AHSA_PRIMARY_COLOR = #003366
AHSA_SECONDARY_COLOR = #FFA500
AHSA_LOGIN_WELCOME_TEXT = Welcome to AHSA Learning Network
AHSA_FOOTER_TEXT = © American High School Academy - AHSA Learning Network
AHSA_ENABLE_BRANDING = true
```

**Alternatively, use environment variables:**

```bash
export AHSA_BRAND_NAME="AHSA Learning Network"
export AHSA_PRIMARY_COLOR="#003366"
export AHSA_SECONDARY_COLOR="#FFA500"
export AHSA_LOGIN_WELCOME_TEXT="Welcome to AHSA Learning Network"
export AHSA_FOOTER_TEXT="© American High School Academy - AHSA Learning Network"
export AHSA_ENABLE_BRANDING=true
```

### 3. Run Migrations

```bash
python manage.py migrate
```

## Branding Setup

### Replace Placeholder Assets

1. Navigate to the theme assets directory:

```bash
cd kolibri/plugins/ahsa_theme/static/assets/ahsa_theme/
```

2. Replace placeholder files with actual AHSA branding:

- `ahsa-logo.svg` - Main SVG logo
- `ahsa-logo-192.png` - 192×192 PNG icon
- `ahsa-logo-512.png` - 512×512 PNG icon
- `ahsa-favicon.ico` - Browser favicon (32×32)
- `ahsa-background.jpg` - Login background (1920×1080 recommended)

3. Collect static files:

```bash
python manage.py collectstatic --noinput
```

### Branding Guidelines

- **Colors**: Navy Blue (#003366) and Orange (#FFA500)
- **Logo**: Should work on light and dark backgrounds
- **File sizes**: Optimize images for web (<500KB each)
- **Background**: Choose an educational, professional image

## Course Seeding

### 1. Validate Blueprints (Dry Run)

Before importing, validate all course blueprints:

```bash
python manage.py seed_ahsa_courses --all --dry-run
```

This checks for:
- Missing required fields
- Invalid data types
- Schema violations
- Structural issues

### 2. Import All Courses

```bash
python manage.py seed_ahsa_courses --all
```

This imports all course blueprints from `kolibri/plugins/ahsa_courses/blueprints/`.

### 3. Verify Import

```bash
# Via Python shell
python manage.py shell

>>> from kolibri.plugins.ahsa_courses.models import CourseBlueprint
>>> CourseBlueprint.objects.count()
4
>>> CourseBlueprint.objects.values_list('course_id', 'title')
```

### 4. Import Individual Courses

```bash
# Import specific course
python manage.py seed_ahsa_courses --course ahsa_alg1

# Import by subject
python manage.py seed_ahsa_courses --subject math

# Import by grade
python manage.py seed_ahsa_courses --grade 9
```

### 5. Update Existing Courses

To re-import and update courses:

```bash
python manage.py seed_ahsa_courses --all --update
```

## Testing

### 1. Start Development Server

```bash
kolibri start --foreground
```

Access at: http://localhost:8000

### 2. Create Test Users

```bash
python manage.py shell

>>> from kolibri.core.auth.models import Facility, FacilityUser
>>> facility = Facility.objects.create(name="AHSA Test School")
>>> admin = FacilityUser.objects.create(
...     username="admin",
...     facility=facility
... )
>>> admin.set_password("admin")
>>> admin.save()
```

### 3. Verify Branding

1. Open browser to http://localhost:8000
2. Check login page shows:
   - AHSA logo
   - AHSA welcome text
   - AHSA background image
   - AHSA colors in navigation

3. Check browser tab shows AHSA favicon

### 4. Test Course API

```bash
# List all courses
curl http://localhost:8000/api/ahsa_courses/courseblueprint/

# Get Algebra 1 details
curl http://localhost:8000/api/ahsa_courses/courseblueprint/1/

# Get NCAA compliance report
curl http://localhost:8000/api/ahsa_courses/courseblueprint/1/ncaa_compliance/
```

### 5. Test Exports

```bash
# Download syllabus
curl -O http://localhost:8000/api/ahsa_courses/courseblueprint/1/download_syllabus/

# Download pacing guide
curl -O http://localhost:8000/api/ahsa_courses/courseblueprint/1/download_pacing_guide/
```

## Production Deployment

### 1. Environment Configuration

```bash
export KOLIBRI_RUN_MODE=production
export KOLIBRI_HOME=/var/kolibri/ahsa
export DJANGO_SETTINGS_MODULE=kolibri.deployment.default.settings.production
```

### 2. Production Settings

Edit `$KOLIBRI_HOME/options.ini`:

```ini
[Server]
CHERRYPY_START = true
CHERRYPY_THREAD_POOL = 150

[Deployment]
PRODUCTION = true

[Branding]
AHSA_BRAND_NAME = AHSA Learning Network
AHSA_PRIMARY_COLOR = #003366
AHSA_SECONDARY_COLOR = #FFA500
AHSA_ENABLE_BRANDING = true

[Paths]
CONTENT_DIR = /var/kolibri/content
```

### 3. System Service (systemd)

Create `/etc/systemd/system/kolibri-ahsa.service`:

```ini
[Unit]
Description=AHSA Learning Network (Kolibri)
After=network.target

[Service]
Type=forking
User=kolibri
Group=kolibri
Environment="KOLIBRI_HOME=/var/kolibri/ahsa"
Environment="KOLIBRI_RUN_MODE=production"
ExecStart=/usr/local/bin/kolibri start
ExecStop=/usr/local/bin/kolibri stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable kolibri-ahsa
sudo systemctl start kolibri-ahsa
sudo systemctl status kolibri-ahsa
```

### 4. Nginx Reverse Proxy

Create `/etc/nginx/sites-available/ahsa-learning`:

```nginx
server {
    listen 80;
    server_name ahsa-learning.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/kolibri/ahsa/content/static/;
        expires 30d;
    }

    location /media/ {
        alias /var/kolibri/ahsa/content/media/;
        expires 30d;
    }
}
```

Enable and reload:

```bash
sudo ln -s /etc/nginx/sites-available/ahsa-learning /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ahsa-learning.example.com
```

### 6. Firewall

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Upgrading Kolibri

### Safe Upgrade Process

1. **Backup Data**

```bash
# Backup database
cp $KOLIBRI_HOME/db.sqlite3 $KOLIBRI_HOME/db.sqlite3.backup

# Backup configuration
cp $KOLIBRI_HOME/options.ini $KOLIBRI_HOME/options.ini.backup

# Backup custom assets
tar -czf ahsa-assets-backup.tar.gz kolibri/plugins/ahsa_theme/static/
```

2. **Test in Staging**

Before upgrading production, test on a staging server with the same setup.

3. **Upgrade Kolibri**

```bash
pip install --upgrade kolibri
```

4. **Run Migrations**

```bash
python manage.py migrate
```

5. **Verify Plugins**

```bash
kolibri plugin list
# Ensure ahsa_theme and ahsa_courses are enabled
```

6. **Test Functionality**

- Login works
- Branding displays correctly
- Course API accessible
- Reports generate properly

7. **Restart Service**

```bash
sudo systemctl restart kolibri-ahsa
```

## Troubleshooting

### Branding Not Showing

**Problem**: Default Kolibri branding still shows

**Solutions**:
1. Verify AHSA theme is enabled: `kolibri plugin list`
2. Disable default theme: `kolibri plugin disable kolibri.plugins.default_theme`
3. Clear browser cache (Ctrl+F5)
4. Run `python manage.py collectstatic`
5. Restart Kolibri

### Course Import Errors

**Problem**: `seed_ahsa_courses` fails with validation errors

**Solutions**:
1. Use `--dry-run` to see detailed errors
2. Check JSON syntax with a validator
3. Verify all required fields are present
4. Check enum values match schema
5. Review error messages for specific issues

### API 403 Forbidden

**Problem**: Cannot access course API

**Solutions**:
1. Ensure user is authenticated
2. Check user has coach or admin role
3. Verify plugin is enabled
4. Check API URL is correct (`/api/ahsa_courses/`)

### Migration Errors

**Problem**: Database migration fails

**Solutions**:
1. Check database file permissions
2. Ensure no running Kolibri instances
3. Backup and try: `python manage.py migrate --fake`
4. Check migration dependencies

### Static Files Not Found

**Problem**: 404 errors for CSS/JS/images

**Solutions**:
1. Run: `python manage.py collectstatic`
2. Check STATIC_ROOT in settings
3. Verify file permissions
4. Check nginx configuration if using reverse proxy

### Memory/Performance Issues

**Problem**: Server slow or crashes

**Solutions**:
1. Increase CherryPy thread pool in options.ini
2. Add more server RAM
3. Enable database connection pooling
4. Use production settings (not dev mode)
5. Monitor with: `kolibri status`

## Advanced Configuration

### Custom Course Blueprints

To add new courses:

1. Create blueprint JSON in `kolibri/plugins/ahsa_courses/blueprints/`
2. Follow schema in `blueprints/README.md`
3. Validate: `python manage.py seed_ahsa_courses --file your_course.json --dry-run`
4. Import: `python manage.py seed_ahsa_courses --file your_course.json`

### Automated Backups

Create cron job:

```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup-script.sh
```

Backup script:

```bash
#!/bin/bash
BACKUP_DIR=/var/backups/kolibri-ahsa
DATE=$(date +\%Y\%m\%d)

# Backup database
cp $KOLIBRI_HOME/db.sqlite3 $BACKUP_DIR/db-$DATE.sqlite3

# Backup options
cp $KOLIBRI_HOME/options.ini $BACKUP_DIR/options-$DATE.ini

# Delete old backups (keep 30 days)
find $BACKUP_DIR -name "db-*.sqlite3" -mtime +30 -delete
```

### Monitoring

Use Kolibri's built-in status:

```bash
kolibri status
```

Monitor logs:

```bash
tail -f $KOLIBRI_HOME/logs/kolibri.txt
```

## Getting Help

1. Review plugin documentation:
   - `kolibri/plugins/ahsa_theme/README.md`
   - `kolibri/plugins/ahsa_courses/README.md`

2. Check Kolibri docs: https://kolibri.readthedocs.io/

3. Review blueprint examples: `kolibri/plugins/ahsa_courses/blueprints/`

4. Contact your Kolibri administrator

## Next Steps

After successful setup:

1. Import content channels (learning materials)
2. Set up facilities and classrooms
3. Create teacher and student accounts
4. Link courses to Kolibri content
5. Configure gradebook and reporting
6. Train teachers on the system
7. Begin student enrollment

---

**Document Version**: 1.0
**Last Updated**: 2026-03-25
**Kolibri Version Tested**: 0.19.x
