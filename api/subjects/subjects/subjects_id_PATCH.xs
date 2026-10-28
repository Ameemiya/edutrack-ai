// Edit subject record belonging to the authenticated user
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id filters=min:1
    text name? filters=trim
    text teacher? filters=trim
    int hours?
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $existing_subject
  
    precondition ($existing_subject != null && $existing_subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Unauthorized access to this subject."
    }
  
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.patch subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = `$input|pick:($raw_input|keys)`
    } as $subject
  }

  response = $subject
  guid = "9iC95ajLd30YBwLjHmezLMXF3L0"
}