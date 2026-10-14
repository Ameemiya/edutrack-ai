// Query all Aluno records
query aluno verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $aluno
  }

  response = $aluno
  guid = "u0xbfroKRF-JWz6otByHptI_j1Q"
}