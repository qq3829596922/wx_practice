curl http://localhost:8012/get_current_user

curl -X POST http://localhost:8012/register -H "Content-Type: application/json" -d '{"username": "alice", "age": 25}'

curl -X POST http://localhost:8012/get_current_user -H "Content-Type: application/json" -d '{"username": "alice", "age": 25}'

curl -X POST http://localhost:8122/sms \                                                             -H "Content-Type: application/json" \                                                             -d '{"access":0}