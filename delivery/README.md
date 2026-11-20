# GRL replay classifier

Everything that gets delivered to mcplayhd: the classifier service and the generated client.

## setup (venv)

```sh
python -m venv .venv
# TODO: activate + pip install -r requirements.txt
# TODO: copy the model files into models/ (see models/README.md)
```

## run

From the `delivery` folder, with the venv active:

```sh
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

- `--host 127.0.0.1`: only reachable from the same machine. Use `--host 0.0.0.0` if the caller runs on another machine or the server runs inside Docker.
- `--port 8000`: any free port works; the client just has to use the same one.
- While developing, add `--reload` to restart on every file save. Leave it out in production.

The models are loaded on the first request (under a second), not at startup.

Docs: `/docs` · spec: `/openapi.json`

## batch size

`POST /label` takes a list of replays. Replays are big (about 70 KB of JSON each, so 300 replays are about 20 MB), and the classification itself is fast (300 replays in about 1.5 s). Send large amounts in **chunks of a few hundred replays** instead of one huge request, so a single request doesn't get too large or slow.

## TODO
- endpoints & what the numbers mean (handbook)
- generating the java client (`scripts/generate_client.sh`)
