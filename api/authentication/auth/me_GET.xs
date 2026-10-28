// Get the record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "created_at"]
    } as $user
  }

  response = $user
  guid = "KYjJ-5j8Dt5lrCc7mjbQysrW3g0"
}