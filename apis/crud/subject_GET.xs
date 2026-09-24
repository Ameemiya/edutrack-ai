// Query all subject records
query subject verb=GET {
  api_group = "CRUD"

  input {
  }

  stack {
    db.query "subject" {
      return = {type: "list"}
    } as $subject
  }

  response = $subject
}
