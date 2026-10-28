table user {
  auth = true

  schema {
    int id
    text name? filters=trim
    email email? filters=trim|lower
    password password? {
      sensitive = true
      visibility = "internal"
    }
  
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "u_Awz-umBQB0iCqolyx2wwxsGQc"
}