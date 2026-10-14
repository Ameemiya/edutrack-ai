// Query all tokens records
query tokens verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $tokens
  }

  response = $tokens
  guid = "ljHGbpR7hH2A-v9qQB-98YK7hqY"
}