// Edit subject record
query "subject/{subject_id}" verb=PATCH {
  api_group = "CRUD"

  input {
    int subject_id
    text name? filters=trim
    text code? filters=trim
    text professor? filters=trim
    text semester? filters=trim
    text status? filters=trim
    text color? filters=trim
    text notes? filters=trim
  }

  stack {
    db.edit "subject" {
      field_value = $input.subject_id
      data = {
        name: $input.name,
        code: $input.code,
        professor: $input.professor,
        semester: $input.semester,
        status: $input.status,
        color: $input.color,
        notes: $input.notes
      }
    } as $subject
  }

  response = $subject
}
