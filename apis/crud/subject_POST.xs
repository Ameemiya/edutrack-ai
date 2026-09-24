// Add subject record
query subject verb=POST {
  api_group = "CRUD"

  input {
    text name filters=trim
    text code? filters=trim
    text professor? filters=trim
    text semester? filters=trim
    text status? filters=trim
    text color? filters=trim
    text notes? filters=trim
  }

  stack {
    db.add "subject" {
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
