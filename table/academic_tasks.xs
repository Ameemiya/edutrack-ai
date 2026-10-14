// Stores academic tasks, homework, and exams tracked by students
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }

    // Title of the academic task
    text title filters=trim

    // Detailed description or instructions for the task
    text description? filters=trim

    // Due date / deadline for the academic task
    date due_date?

    // Current status of the task (e.g. pending, in_progress, completed)
    text status?="pending" filters=trim

    // Reference to the associated subject in the subjects table
    int subject_id? {
      table = "subjects"
    }

    // Reference to the authenticated user in the users table
    int user_id? {
      table = "users"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "subject_id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "due_date"}]}
  ]
  guid = "XSYmSlDXMIUqxqWMkcUI814yHaY"
}

