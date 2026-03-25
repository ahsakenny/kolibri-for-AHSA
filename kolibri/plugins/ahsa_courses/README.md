# AHSA Courses Plugin Documentation

## Overview

The AHSA Courses Plugin provides a comprehensive course blueprint system for AHSA Learning Network. It enables creation, management, and documentation of structured courses aligned with Florida state standards and designed to support NCAA approval workflows.

## Features

- **Course Blueprint Models**: Comprehensive data models for courses, weeks, lessons, and assessments
- **Florida Standards Alignment**: Track and report on standards coverage
- **NCAA Compliance Tools**: Generate compliance reports and documentation
- **Course Seeding**: Import course structures from JSON/YAML blueprints
- **Reporting & Exports**: Syllabus, pacing guides, and standards alignment reports
- **API Access**: Full REST API for course management

## Installation & Activation

### 1. Enable the Plugin

```bash
kolibri plugin enable kolibri.plugins.ahsa_courses
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Seed Course Blueprints

```bash
python manage.py seed_ahsa_courses --all
```

### 4. Restart Kolibri

```bash
kolibri stop
kolibri start
```

## Data Models

### CourseBlueprint
Main course model containing:
- Course metadata (title, description, grade level, subject)
- Florida standards reference
- NCAA classification and compliance metadata
- Credit value and duration
- Syllabus and pacing information

### Week
Weekly units within a course:
- Week number and title
- Learning objectives
- Standards alignment
- Teacher interaction requirements

### LessonPlan
Individual lessons within a week:
- Lesson content and activities
- Video and reading resource placeholders (OER)
- Estimated instructional time

### Assessment
Course assessments:
- Type (quiz, test, exam, project, written assignment)
- Proctoring requirements
- Grading rubrics
- Point values and weights

### Semester
Semester grouping (for full-year courses):
- Semester number (1 or 2)
- Credit value
- Week assignments

### GradeCategory
Grading categories:
- Category name and weight
- Drop lowest policy

## API Endpoints

### Course Blueprints

**List all courses:**
```
GET /api/ahsa_courses/courseblueprint/
```

**Filter by grade, subject, or NCAA area:**
```
GET /api/ahsa_courses/courseblueprint/?grade_level=9&subject=math
GET /api/ahsa_courses/courseblueprint/?ncaa_core_area=mathematics
```

**Get course details:**
```
GET /api/ahsa_courses/courseblueprint/{id}/
```

**Get course syllabus:**
```
GET /api/ahsa_courses/courseblueprint/{id}/syllabus/
```

**Get pacing summary:**
```
GET /api/ahsa_courses/courseblueprint/{id}/pacing_summary/
```

**Get standards alignment report:**
```
GET /api/ahsa_courses/courseblueprint/{id}/standards_alignment/
```

**Get NCAA compliance report:**
```
GET /api/ahsa_courses/courseblueprint/{id}/ncaa_compliance/
```

**Download syllabus (text file):**
```
GET /api/ahsa_courses/courseblueprint/{id}/download_syllabus/
```

**Download pacing guide (CSV):**
```
GET /api/ahsa_courses/courseblueprint/{id}/download_pacing_guide/
```

### Other Endpoints

```
GET /api/ahsa_courses/week/
GET /api/ahsa_courses/lessonplan/
GET /api/ahsa_courses/assessment/
GET /api/ahsa_courses/gradecategory/
```

## Management Commands

### seed_ahsa_courses

Import course blueprints from JSON/YAML files.

**Seed all courses:**
```bash
python manage.py seed_ahsa_courses --all
```

**Seed specific course:**
```bash
python manage.py seed_ahsa_courses --course ahsa_alg1
```

**Seed by subject:**
```bash
python manage.py seed_ahsa_courses --subject math
```

**Seed by grade:**
```bash
python manage.py seed_ahsa_courses --grade 9
```

**Seed from custom file:**
```bash
python manage.py seed_ahsa_courses --file /path/to/blueprint.json
```

**Validate without importing (dry run):**
```bash
python manage.py seed_ahsa_courses --all --dry-run
```

**Update existing courses:**
```bash
python manage.py seed_ahsa_courses --all --update
```

## NCAA Compliance Features

### Compliance Checklist

The NCAA compliance report (`/ncaa_compliance/` endpoint) checks:

1. **Core Classification**: Course is classified in an NCAA core area
2. **Teacher-Led Instruction**: Course requires active teacher oversight
3. **Instructional Time**: Minimum 140 hours for full-year courses
4. **Proctored Assessments**: Midterm and final exams are proctored
5. **Academic Integrity**: Academic integrity policy is documented
6. **Teacher Interaction**: Regular teacher interaction throughout course (≥75% of weeks)

### Syllabus Export

Generate NCAA-compliant syllabus documents including:
- Course information and metadata
- Instructional time breakdown
- Required materials
- Grading policy
- Pacing guide
- Weekly schedule with objectives
- Academic integrity policy

Export formats:
- Text file (download_syllabus endpoint)
- JSON (syllabus endpoint)

### Pacing Guide Export

Export detailed week-by-week pacing guides:
- CSV format with standards alignment
- Lesson and assessment counts
- Teacher interaction requirements
- Estimated instructional minutes

## Course Blueprint Development

### Creating Blueprints

See `blueprints/README.md` for detailed blueprint specification.

Example structure:
```json
{
  "course_id": "ahsa_alg1",
  "title": "Algebra 1",
  "grade_level": 9,
  "subject": "math",
  "ncaa_core_area": "mathematics",
  "credit_value": 1.0,
  "total_weeks": 36,
  "weeks": [...],
  "grade_categories": [...]
}
```

### Validation

All blueprints are validated against a JSON schema before import:
- Required fields checked
- Enum values validated
- Data types enforced
- Relationships verified

## Example Usage

### Python API

```python
from kolibri.plugins.ahsa_courses.models import CourseBlueprint

# Get all algebra courses
algebra_courses = CourseBlueprint.objects.filter(
    subject='math',
    title__icontains='algebra'
)

# Get NCAA core courses for grade 9
ncaa_courses = CourseBlueprint.objects.filter(
    grade_level=9
).exclude(ncaa_core_area='none')

# Get course with all related data
course = CourseBlueprint.objects.prefetch_related(
    'weeks__lesson_plans',
    'weeks__assessments',
    'grade_categories'
).get(course_id='ahsa_alg1')

# Calculate total instructional time
total_hours = course.total_instructional_minutes / 60
```

### Generating Reports

```python
from kolibri.plugins.ahsa_courses.reports import (
    NCAAComplianceReporter,
    NCAASyllabusExporter,
    StandardsAlignmentReporter
)

# Generate compliance report
course = CourseBlueprint.objects.get(course_id='ahsa_alg1')
compliance = NCAAComplianceReporter.generate_compliance_report(course)

# Export syllabus
syllabus_text = NCAASyllabusExporter.export_to_text(course)

# Generate standards report
standards = StandardsAlignmentReporter.generate_alignment_report(course)
```

## Integration with Kolibri

### Linking to Kolibri Collections

Courses can be optionally linked to Kolibri classrooms/collections:

```python
from kolibri.core.auth.models import Collection

classroom = Collection.objects.get(name="Grade 9 Mathematics")
course.collection = classroom
course.save()
```

### Content Mapping

Lesson plans can reference Kolibri content nodes:

```python
lesson.contentnode_id = "1234567890abcdef"
lesson.save()
```

## Best Practices

### Course Design

1. **Align to Standards**: Reference specific Florida standards in each week
2. **Consistent Pacing**: Maintain 225 minutes/week (45 min/day × 5 days)
3. **Regular Assessments**: Include weekly quizzes and periodic tests
4. **Teacher Interaction**: Mark weeks requiring teacher touchpoints
5. **NCAA Requirements**: For core courses, ensure proctored exams and teacher oversight

### NCAA Approval Workflow

1. Design course with NCAA core area classification
2. Ensure minimum 140 hours instructional time
3. Include proctored midterm and final exams
4. Document academic integrity policy
5. Mark course as teacher-led
6. Generate compliance report
7. Export syllabus for submission
8. Submit to NCAA for approval
9. Update `is_ncaa_approved` flag when approved

### Maintenance

- **Version Control**: Increment `version` field when updating blueprints
- **Backup**: Export blueprints to JSON before major changes
- **Testing**: Use `--dry-run` to validate changes before importing
- **Documentation**: Keep `teacher_notes` updated with implementation guidance

## Troubleshooting

### Import Errors

**"Course already exists"**
- Use `--update` flag to overwrite
- Or change the `course_id` in blueprint

**"Validation errors"**
- Check required fields are present
- Verify enum values (subject, ncaa_core_area, etc.)
- Ensure week numbers are sequential

**"File not found"**
- Use absolute paths
- Check blueprint is in `blueprints/` directory

### API Access

**403 Forbidden**
- Ensure user has appropriate permissions (admin or coach)
- Check authentication token

**404 Not Found**
- Verify course ID is correct
- Ensure course was successfully imported

## Future Enhancements

Potential features for future development:

- Visual course builder UI
- Student enrollment and progress tracking
- Gradebook integration
- Assignment submission workflow
- Parent/student portal views
- Automated standards coverage analysis
- Integration with external OER repositories
- Course cloning and customization tools
- Batch operations for course management

## Support & Contributing

For issues, questions, or enhancements:

1. Review this documentation
2. Check the blueprint schema and examples
3. Test with `--dry-run` mode
4. Review API endpoint documentation
5. Contact your Kolibri administrator

## License

This plugin extends Kolibri and maintains the same MIT License.
Course blueprints reference OER content which maintains original licenses (CC BY, etc.).

## See Also

- AHSA Theme Plugin: `kolibri/plugins/ahsa_theme/`
- Course Blueprints: `blueprints/README.md`
- Kolibri Plugin Documentation: `docs/backend_architecture/plugins.rst`
- Kolibri API Patterns: `docs/backend_architecture/api_patterns.rst`
