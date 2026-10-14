// Query all STATUS_TESTORNO records
query status_testorno verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_testorno
  }

  response = $status_testorno
  guid = "jwL41L7FGUddE1cG_I7KMKYz02M"
}