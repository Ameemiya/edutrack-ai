// Query all PAPEL records
query papel verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $papel
  }

  response = $papel
  guid = "Vb8VfH0AzvQhBqjfib-tJyWiC8s"
}