# AHSA Course Blueprints

This directory contains JSON blueprint files for AHSA Learning Network courses.

## Available Blueprints

### High School Core Courses
- **ahsa_alg1.json** - Algebra 1 (Grade 9, NCAA Math Core)
- **ahsa_bio.json** - Biology (Grade 9, NCAA Natural Science Core)
- **ahsa_eng1.json** - English 1 (Grade 9, NCAA English Core)

### Middle School Core Courses
- **ahsa_g6_math.json** - Grade 6 Mathematics

## Blueprint Structure

Each blueprint follows this schema:

```json
{
  "course_id": "unique_course_identifier",
  "title": "Course Title",
  "description": "Course description",
  "grade_band": "middle|high",
  "grade_level": 6-12,
  "subject": "ela|math|science|social_studies|elective",
  "florida_standard_set": "FL standards reference",
  "ncaa_core_area": "english|mathematics|natural_science|social_science|additional|none",
  "duration": "full_year|semester|quarter",
  "credit_value": 0.0-2.0,
  "total_weeks": 36,
  "weekly_minutes": 225,
  "grade_categories": [...],
  "weeks": [...]
}
```

## Importing Blueprints

### Import All Courses
```bash
python manage.py seed_ahsa_courses --all
```

### Import Specific Course
```bash
python manage.py seed_ahsa_courses --course ahsa_alg1
```

### Import by Subject
```bash
python manage.py seed_ahsa_courses --subject math
```

### Dry Run (Validation Only)
```bash
python manage.py seed_ahsa_courses --all --dry-run
```

### Update Existing Courses
```bash
python manage.py seed_ahsa_courses --all --update
```

## Creating New Blueprints

1. Copy an existing blueprint as a template
2. Update all course metadata
3. Define weeks with objectives and standards alignment
4. Add lesson plans and assessments
5. Validate with: `python manage.py seed_ahsa_courses --file your_blueprint.json --dry-run`
6. Import with: `python manage.py seed_ahsa_courses --file your_blueprint.json`

## Blueprint Guidelines

### Florida Standards Alignment
- Reference specific Florida state standards in `florida_standard_set`
- List specific standards in each week's `standards_alignment` array
- Ensure comprehensive coverage across the course

### NCAA Requirements
- Set `ncaa_core_area` appropriately for core academic courses
- Ensure `teacher_led` is true for NCAA courses
- Include proctoring requirements for exams
- Document teacher interaction points in weeks

### Pacing
- Full-year courses: 36 weeks
- Semester courses: 18 weeks
- Default to 225 minutes/week (45 min/day × 5 days)
- Include midterm (week 18) and final (week 36) for full-year courses

### Assessment Structure
- Include weekly quizzes (auto-graded when possible)
- Add unit tests at regular intervals
- Require proctored midterm and final exams
- For labs/essays, set `has_teacher_grading: true`

### Resource Placeholders
- Use OER resources (OpenStax, Khan Academy, CK-12)
- Include URLs and license information
- Specify resource type (textbook, video, software, lab)

## Validation

Blueprints are validated against a JSON schema. Common validation errors:

- Missing required fields (course_id, title, grade_level, etc.)
- Invalid enum values (subject, ncaa_core_area, duration)
- Week numbers not sequential
- Missing required week fields

Run validation:
```bash
python manage.py seed_ahsa_courses --file your_blueprint.json --dry-run
```

## Versioning

- Set `version` field (e.g., "1.0", "1.1")
- Increment version when making significant changes
- Document changes in course `description` or `teacher_notes`

## Contributing

When adding new course blueprints:

1. Follow the naming convention: `ahsa_<subject>_<grade/level>.json`
2. Ensure Florida standards are accurate
3. Include NCAA metadata where applicable
4. Provide realistic pacing and time estimates
5. Include placeholder OER resources with proper attribution
6. Test import with `--dry-run` first
7. Document any special requirements in the blueprint

## License

Course blueprints are designed for AHSA Learning Network.
OER resource references maintain their original licenses (CC BY, etc.).
