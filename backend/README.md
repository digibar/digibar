# Backend

For development with local dev server:

```sh
docker run -p 127.0.0.1:6379:6379 --name redissvr -d redis:alpine
```

## Test data

Run `testdata.sh` with the port number of the Python server to populate the system with some dummy data. The port number usually is 5000 (local) or 8000 (Docker)