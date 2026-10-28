// Query all subjects belonging to the authenticated user
query subjects verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      where = [{field: "user_id", op: "==", value: $auth.id}] == true
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  guid = "bL_CIpTl4oPJ_a0ItczzSttG8QE"
}