// Edit academic task belonging to the authenticated user
query "academic_tasks/{academic_tasks_id}" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int academic_tasks_id filters=min:1
    text title? filters=trim
    text description? filters=trim
    date due_date?
    text status? filters=trim
    int subject_id?
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    } as $existing_task
  
    precondition ($existing_task != null && $existing_task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Unauthorized access to this academic task."
    }
  
    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        subject_id : $input.subject_id
      }
    } as $task
  }

  response = $task
  guid = "gnrI5dfil4QjnT8FPWfJBPME5hg"
}