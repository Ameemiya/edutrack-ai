// Add STATUS_PEDIDO record
query status_pedido verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_pedido
  }

  response = $status_pedido
  guid = "5iiNV5J_gINr1k8FfFV-lmW6fh0"
}