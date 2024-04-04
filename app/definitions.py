class CognitoIdentity:
  cognito_identity_id: str | None
  cognito_identity_pool_id: str | None

class LambdaContext:
  function_name: str
  function_version: str
  invoked_function_arn: str
  memory_limit_in_mb: str
  aws_request_id: str
  log_group_name: str
  log_stream_name: str
  identity: CognitoIdentity