// Query all Cliente records
query cliente verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $cliente
  }

  response = $cliente
  guid = "oEE-1m2t9gqHyKJQkDvBh40_3Zs"
}