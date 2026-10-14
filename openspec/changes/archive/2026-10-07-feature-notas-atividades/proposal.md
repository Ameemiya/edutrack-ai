## Why

Teachers using EduTrack AI need the ability to submit grades for students on specific academic activities to keep track of academic performance and evaluations.

## What Changes

- Create the `activity_grades` database table to store student grades for activities.
- Create the `POST /activity_grades` API endpoint to allow teachers to submit a grade for a student on a specific activity.
- Associate each grade submission with the student, activity, and authenticated teacher user ID.

## Capabilities

### New Capabilities
- `activity-grades`: Defines the data storage and submission API for teacher grading of student activities.

### Modified Capabilities
*(None)*

## Impact

- **Backend**: Adds `tables/activity_grades.xs` and `apis/activity_grades/activity_grades_POST.xs` in Xano.
- **Data Model**: Introduces `activity_grades` with relations to students (`user_id`), activities (`task_id`), and grade values.
