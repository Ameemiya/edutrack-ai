// Stores academic subjects tracked by users
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // Name of the academic subject
    text name filters=trim
  
    // Teacher or instructor name
    text teacher? filters=trim
  
    // Workload hours for the subject
    int hours?
  
    int user_id? {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "Vkp5xWW1BhQex5NPsWQToMA3FxY"
}