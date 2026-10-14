// Query all user records
query user verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $user
  }

  response = $user
  guid = "nEeVBHJnXy9J4g2H8FxMiZnXi08"
}