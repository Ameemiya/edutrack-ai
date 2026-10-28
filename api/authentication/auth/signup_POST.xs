// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text name?
    email email? filters=lower|trim
    password password?
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    precondition ($user == null) {
      error_type = "accessdenied"
      error = "This account is already in use."
    }
  
    db.add user {
      enforce_hidden_fields = false
      data = {
        name      : $input.name
        email     : $input.email
        password  : $input.password
        created_at: "now"
      }
    } as $user
  
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "qjFhJQm90gY-Kv32rfUp53mQjCI"
}