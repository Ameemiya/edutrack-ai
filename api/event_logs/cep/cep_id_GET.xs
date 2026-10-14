// Get CEP record
query "cep/{cep_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int cep_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.cep_id
    } as $cep
  
    precondition ($cep != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $cep
  guid = "RcOHuxY2C1dwKgQ5JdmDTd4y1es"
}