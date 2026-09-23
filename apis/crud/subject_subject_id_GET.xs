// Get a single subject record
query "subject/{subject_id}" verb=GET {
  api_group = "CRUD"

  input {
    int subject_id
  }

  stack {
    db.get "subject" {
      field_value = $input.subject_id
    } as $subject
  }

  response = $subject
}
