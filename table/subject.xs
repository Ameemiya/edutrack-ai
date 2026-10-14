// Stores academic subjects and course details
// Adiciona Materias
table subject {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // Name of the subject
    text name filters=trim
  
    // Course or subject code
    text code? filters=trim
  
    // Professor or instructor name
    text professor? filters=trim
  
    // Academic semester or period
    text semester? filters=trim
  
    // Status of the subject (e.g. Ativa, Concluída, Trancada)
    text status? filters=trim
  
    // Color tag or hex code for UI representation
    text color? filters=trim
  
    // Additional notes or observations
    text notes? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "status"}]}
  ]

  guid = "_PwdhwrNd4ngAmN4EmRfs9_1SyE"
}