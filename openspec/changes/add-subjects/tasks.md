## 1. Schema and Backend Definition

- [x] 1.1 Define subject table schema in XanoScript (`tables/subject.xs`)
- [x] 1.2 Define subject CRUD API endpoint definitions in XanoScript (`apis/crud/`)

## 2. Service Layer Implementation

- [x] 2.1 Create `services/subject_service.py` with CRUD methods for subject management
- [x] 2.2 Implement session state fallback in `subject_service.py` for offline/local development
- [x] 2.3 Add validation checks for subject name and status values

## 3. Frontend Integration in Streamlit

- [x] 3.1 Implement subject listing in `app.py` under "Disciplinas" with cards/table view
- [x] 3.2 Add subject creation form with required fields and error handling
- [x] 3.3 Add subject edit and delete actions
- [x] 3.4 Update Dashboard metric "Disciplinas Ativas" to reflect active subjects count

## 4. Testing and Verification

- [x] 4.1 Verify subject creation, updating, and deletion workflow in Streamlit
- [x] 4.2 Verify dashboard metrics accurately calculate active subjects

