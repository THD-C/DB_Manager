# DB_Manager
### build proto
`python -m grpc_tools.protoc -I=./Protocol/proto/ --python_out=. --grpc_python_out=. --pyi_out=. user/user.proto`

## Startup

1. `docker compose build`
2. `docker compose up -d`
