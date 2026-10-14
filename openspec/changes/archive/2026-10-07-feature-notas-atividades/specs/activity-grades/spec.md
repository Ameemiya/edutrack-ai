# activity-grades Specification

## Purpose

Enables teachers to submit and record grades for students on specific academic activities in EduTrack AI.

## ADDED Requirements

### Requirement: Grade Submission Table
The system SHALL store student grades for activities in the `activity_grades` table, capturing student ID, activity ID, grade value, and feedback.

#### Scenario: Store activity grade
- **WHEN** a grade is recorded for a student on an activity
- **THEN** the system stores the entry with student reference (`user_id`), activity reference, grade value, and timestamp

### Requirement: Submit Activity Grade Endpoint
The system SHALL provide a `POST /activity_grades` API endpoint that allows teachers to submit a grade for a student on a specific activity.

#### Scenario: Successful grade submission
- **WHEN** a teacher sends a `POST /activity_grades` request with valid student ID, activity ID, and numeric grade
- **THEN** the system creates the grade record and returns the created grade details

#### Scenario: Missing required parameters
- **WHEN** a grade submission request is sent without required student ID, activity ID, or grade
- **THEN** the system SHALL reject the request with an appropriate validation error
