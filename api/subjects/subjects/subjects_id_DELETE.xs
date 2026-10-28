// Delete subject record belonging to the authenticated user
query "subjects/{subjects_id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id filters=min:1
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
  
    db.del subjects {
      field_name = "id"
      field_value = $input.subjects_id
    }
  }

  response = {success: true}
  guid = "x2Rez4CpJbJ32D-_J09vPLVcUjc"
}