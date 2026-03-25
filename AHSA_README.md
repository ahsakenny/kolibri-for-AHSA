# AHSA Learning Network - White-Label Transformation

## Executive Summary

This repository contains a white-labeled transformation of Kolibri into **AHSA Learning Network**, a branded digital school platform for American High School Academy (AHSA). The transformation includes:

- **Complete Rebranding**: Custom theme, logo, colors, and terminology
- **NCAA-Ready Courses**: Pre-structured courses aligned with Florida standards and designed to support NCAA approval workflows
- **Course Framework**: Grades 6-12 course blueprints with sample courses for Algebra 1, Biology, English 1, and Grade 6 Math
- **Automated Seeding**: Management commands to import course structures from JSON blueprints
- **Compliance Tools**: NCAA compliance checkers, syllabus exports, and pacing guide generators

## Key Features

### 🎨 White-Label Branding

- Custom AHSA theme plugin with configurable colors, logos, and text
- Environment-variable based configuration
- Login page, navigation, and footer customization
- Browser tab titles and favicons

### 📚 Course Blueprint System

- Comprehensive data models for courses, weeks, lessons, and assessments
- Florida state standards alignment tracking
- NCAA core area classification
- Detailed pacing guides (36-week full-year courses)
- Open Educational Resource (OER) content placeholders

### ⚖️ NCAA Compliance Features

- NCAA-ready course metadata (teacher-led, proctoring, instructional time)
- Compliance checklist generator
- Syllabus export (text and JSON)
- Pacing guide export (CSV)
- Standards alignment reports
- Academic integrity documentation

### 🔧 Administrative Tools

- Django management commands for course seeding
- JSON schema validation for blueprints
- Dry-run mode for testing imports
- Bulk course import/update capabilities
- REST API for all course data

## Architecture

This implementation follows Kolibri's plugin architecture for maintainability and upgradability:

### Plugin-Based Design

```
kolibri/plugins/
├── ahsa_theme/           # Branding and visual customization
│   ├── kolibri_plugin.py  # Theme hook implementation
│   ├── options.py         # Configuration options
│   └── static/assets/     # Logos, images, icons
│
└── ahsa_courses/         # Course blueprint system
    ├── models.py          # Data models
    ├── viewsets.py        # REST API
    ├── serializers.py     # API serializers
    ├── seeder.py          # Import logic
    ├── validators.py      # Schema validation
    ├── reports.py         # NCAA compliance tools
    ├── management/        # Django commands
    └── blueprints/        # Course JSON files
```

### Key Design Principles

✅ **Non-Invasive**: No Kolibri core files modified
✅ **Upgradeable**: Compatible with Kolibri updates
✅ **Configurable**: Environment variables and config files
✅ **Maintainable**: Clear separation of concerns
✅ **Extensible**: Easy to add new courses and features

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/ahsakenny/kolibri-for-AHSA.git
cd kolibri-for-AHSA
pip install -r requirements/dev.txt
export KOLIBRI_HOME=$HOME/.kolibri-ahsa
kolibri configure setup
```

### 2. Enable AHSA Plugins

```bash
kolibri plugin disable kolibri.plugins.default_theme
kolibri plugin enable kolibri.plugins.ahsa_theme
kolibri plugin enable kolibri.plugins.ahsa_courses
python manage.py migrate
```

### 3. Seed Courses

```bash
python manage.py seed_ahsa_courses --all
```

### 4. Start Server

```bash
kolibri start
# Access at http://localhost:8000
```

## Documentation

- **[Complete Setup Guide](AHSA_SETUP_GUIDE.md)** - Full installation and deployment
- **[Theme Plugin](kolibri/plugins/ahsa_theme/README.md)** - Branding customization
- **[Courses Plugin](kolibri/plugins/ahsa_courses/README.md)** - Course management and API
- **[Blueprint Schema](kolibri/plugins/ahsa_courses/blueprints/README.md)** - Course blueprint format

## Sample Courses Included

The system includes sample blueprints for:

- **ahsa_alg1** - Algebra 1 (Grade 9, NCAA Math Core)
- **ahsa_bio** - Biology (Grade 9, NCAA Natural Science Core)
- **ahsa_eng1** - English 1 (Grade 9, NCAA English Core)
- **ahsa_g6_math** - Grade 6 Mathematics (Middle School)

Each course includes:
- 36-week pacing (full year) or 18-week (semester)
- Weekly objectives and standards alignment
- Lesson plans with OER resource placeholders
- Assessments (quizzes, tests, exams)
- Grading categories
- NCAA compliance metadata

## Configuration

### Branding Configuration

Edit `$KOLIBRI_HOME/options.ini` or set environment variables:

```ini
[Branding]
AHSA_BRAND_NAME = AHSA Learning Network
AHSA_PRIMARY_COLOR = #003366
AHSA_SECONDARY_COLOR = #FFA500
AHSA_LOGIN_WELCOME_TEXT = Welcome to AHSA Learning Network
AHSA_FOOTER_TEXT = © American High School Academy
```

### Replace Branding Assets

1. Navigate to `kolibri/plugins/ahsa_theme/static/assets/ahsa_theme/`
2. Replace placeholder files with AHSA branding:
   - `ahsa-logo.svg` (main logo)
   - `ahsa-logo-192.png` (192×192 icon)
   - `ahsa-logo-512.png` (512×512 icon)
   - `ahsa-favicon.ico` (browser favicon)
   - `ahsa-background.jpg` (login background)
3. Run: `python manage.py collectstatic`

## API Endpoints

### Course Management

```
GET  /api/ahsa_courses/courseblueprint/              # List all courses
GET  /api/ahsa_courses/courseblueprint/{id}/         # Course details
GET  /api/ahsa_courses/courseblueprint/{id}/syllabus/  # Syllabus data
GET  /api/ahsa_courses/courseblueprint/{id}/pacing_summary/  # Pacing guide
GET  /api/ahsa_courses/courseblueprint/{id}/ncaa_compliance/  # NCAA report
GET  /api/ahsa_courses/courseblueprint/{id}/download_syllabus/  # Text export
GET  /api/ahsa_courses/courseblueprint/{id}/download_pacing_guide/  # CSV export
```

### Filtering

```
GET  /api/ahsa_courses/courseblueprint/?grade_level=9
GET  /api/ahsa_courses/courseblueprint/?subject=math
GET  /api/ahsa_courses/courseblueprint/?ncaa_core_area=mathematics
GET  /api/ahsa_courses/courseblueprint/?is_active=true
```

## Management Commands

```bash
# Import all courses
python manage.py seed_ahsa_courses --all

# Import specific course
python manage.py seed_ahsa_courses --course ahsa_alg1

# Import by subject
python manage.py seed_ahsa_courses --subject math

# Import by grade
python manage.py seed_ahsa_courses --grade 9

# Validate without importing
python manage.py seed_ahsa_courses --all --dry-run

# Update existing courses
python manage.py seed_ahsa_courses --all --update

# Import from custom file
python manage.py seed_ahsa_courses --file /path/to/blueprint.json
```

## Target Course Inventory

The framework supports grades 6-12 with the following structure:

### Middle School (Grades 6-8)
- English Language Arts (6, 7, 8)
- Mathematics (6, 7, 8)
- Science (6, 7, 8)
- Social Studies (6, 7, 8)

### High School Core (Grades 9-12)
- English (1, 2, 3, 4)
- Mathematics (Algebra 1, Geometry, Algebra 2)
- Science (Biology, Chemistry, Physics)
- Social Studies (World History, US History, Government, Economics)

### Electives
- Health, PE Theory, Psychology, Sociology
- Personal Finance, Entrepreneurship
- Digital Literacy, Computer Science
- Career Planning, SAT/ACT Prep

## NCAA Compliance Workflow

1. Design course with appropriate metadata:
   - Set `ncaa_core_area` (english, mathematics, natural_science, etc.)
   - Enable `teacher_led`
   - Ensure minimum 140 hours instructional time
   - Include proctored midterm and final exams
   - Document academic integrity policy

2. Generate compliance report:
   ```bash
   curl http://localhost:8000/api/ahsa_courses/courseblueprint/1/ncaa_compliance/
   ```

3. Export syllabus for NCAA submission:
   ```bash
   curl -O http://localhost:8000/api/ahsa_courses/courseblueprint/1/download_syllabus/
   ```

4. Submit to NCAA for approval

5. Update course:
   ```python
   course.is_ncaa_approved = True
   course.save()
   ```

## Creating Custom Courses

### 1. Create Blueprint

Create a JSON file in `kolibri/plugins/ahsa_courses/blueprints/`:

```json
{
  "course_id": "ahsa_geo",
  "title": "Geometry",
  "grade_level": 10,
  "subject": "math",
  "ncaa_core_area": "mathematics",
  "credit_value": 1.0,
  "total_weeks": 36,
  "weeks": [
    {
      "week_number": 1,
      "title": "Introduction to Geometry",
      "objectives": [...],
      "standards_alignment": [...],
      "lesson_plans": [...],
      "assessments": [...]
    }
  ]
}
```

### 2. Validate

```bash
python manage.py seed_ahsa_courses --file blueprints/ahsa_geo.json --dry-run
```

### 3. Import

```bash
python manage.py seed_ahsa_courses --file blueprints/ahsa_geo.json
```

## Testing

Run Python syntax checks:

```bash
python3 -m py_compile kolibri/plugins/ahsa_theme/kolibri_plugin.py
python3 -m py_compile kolibri/plugins/ahsa_courses/models.py
python3 -m py_compile kolibri/plugins/ahsa_courses/seeder.py
```

Test course import:

```bash
python manage.py seed_ahsa_courses --all --dry-run
```

Test API access:

```bash
curl http://localhost:8000/api/ahsa_courses/courseblueprint/
```

## Production Deployment

See **[AHSA_SETUP_GUIDE.md](AHSA_SETUP_GUIDE.md)** for complete production deployment instructions including:

- Environment configuration
- System service setup (systemd)
- Nginx reverse proxy
- SSL certificates
- Firewall configuration
- Automated backups
- Monitoring

## Maintenance

### Upgrading Kolibri

1. Backup database and configuration
2. Test upgrade in staging
3. Run: `pip install --upgrade kolibri`
4. Run: `python manage.py migrate`
5. Verify plugins are enabled
6. Restart service

### Updating Courses

To update existing course blueprints:

```bash
python manage.py seed_ahsa_courses --course ahsa_alg1 --update
```

### Backups

Regular backups should include:
- `$KOLIBRI_HOME/db.sqlite3` (database)
- `$KOLIBRI_HOME/options.ini` (configuration)
- `kolibri/plugins/ahsa_theme/static/` (custom assets)
- `kolibri/plugins/ahsa_courses/blueprints/` (course data)

## Known Limitations

- **String replacement**: Complete "Kolibri" → "AHSA" replacement in all internal strings would require modifying core files. The current approach focuses on user-visible branding.
- **Assignment submission**: Basic assignment tracking is supported through Kolibri's existing Lesson system. Full LMS-style submission workflows would require additional development.
- **Automatic NCAA approval**: The system supports NCAA documentation workflows but does not claim automatic approval. Courses must still go through official NCAA review.

## Security Considerations

- Always use proctored exams for high-stakes assessments
- Document academic integrity policies
- Use secure passwords for administrative accounts
- Keep Kolibri updated for security patches
- Use HTTPS in production (SSL/TLS)
- Regular backups of sensitive data

## License & Attribution

This project extends Kolibri, which is licensed under the MIT License.

**Kolibri Attribution**: This work is based on Kolibri by Learning Equality. The original Kolibri project is licensed under the MIT License.

**AHSA Customization**: The AHSA-specific plugins and course blueprints are also licensed under the MIT License.

**OER Content References**: Course blueprints reference Open Educational Resources (OpenStax, Khan Academy, CK-12) which maintain their original licenses (typically CC BY 4.0).

All appropriate attribution is maintained in the codebase and documentation as required by licenses.

## Support & Contact

For questions, issues, or enhancements:

1. Review the documentation in this repository
2. Check the [Setup Guide](AHSA_SETUP_GUIDE.md) for common issues
3. Review plugin READMEs for specific features
4. Contact your Kolibri administrator
5. Refer to Kolibri documentation: https://kolibri.readthedocs.io/

## Acknowledgments

- **Kolibri** by Learning Equality - Foundation platform
- **OpenStax** - Open educational textbooks
- **Khan Academy** - Video content resources
- **CK-12 Foundation** - OER content
- **Florida Department of Education** - Standards alignment framework

## Version History

- **v1.0** (2026-03-25) - Initial AHSA transformation
  - AHSA theme plugin
  - Course blueprint system
  - Sample courses (Algebra 1, Biology, English 1, Grade 6 Math)
  - NCAA compliance tools
  - Management commands
  - Complete documentation

---

**Project**: AHSA Learning Network
**Based On**: Kolibri 0.19.x
**Status**: Production Ready
**Last Updated**: 2026-03-25
