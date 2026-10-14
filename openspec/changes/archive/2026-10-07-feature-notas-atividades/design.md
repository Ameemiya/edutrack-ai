## Context

Teachers in EduTrack AI need an API endpoint and a database structure to grade student assignments. Following the strict scope rule in `AGENTS.md`, only the requested table and submission endpoint are planned.

## Goals / Non-Goals

**Goals:**
- Define the `activity_grades` table schema in XanoScript to store grades.
- Define the `POST /activity_grades` endpoint in XanoScript for grade submission.

**Non-Goals:**
- Creating grade listing endpoints (`GET /academic_tasks/{id}/grades`, `GET /users/{id}/grades`) as they were not requested.
- Frontend modifications or test suites (not explicitly requested).

## Decisions

### 1. Data Model (`activity_grades`)
- `id`: integer auto-increment primary key
- `created_at`: timestamp
- `user_id`: integer foreign key referencing the student in table `user`
- `task_id`: integer referencing the academic task/activity
- `grade`: decimal/number representing the grade score
- `feedback`: optional text comment
- `teacher_id`: integer foreign key referencing the teacher in table `user`

### 2. Submission Endpoint (`POST /activity_grades`)
- Accepts `user_id`, `task_id`, `grade`, and optional `feedback`.
- Validates that mandatory parameters are provided before inserting the record.

## Risks / Trade-offs

- **[Risk] Grade updates for already graded activities**
  → **Mitigation**: Future changes can introduce an update endpoint (`PATCH /activity_grades/{id}`) if required; `POST` creates a new grading record.
