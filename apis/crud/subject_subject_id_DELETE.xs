// Delete subject record
query "subject/{subject_id}" verb=DELETE {
  api_group = "CRUD"

  input {
    int subject_id
  }

  stack {
    db.delete "subject" {
      field_value = $input.subject_id
    } as $subject
  }

  response = $subject
}
