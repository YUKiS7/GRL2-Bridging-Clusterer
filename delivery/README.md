# GRL replay classifier

Everything that gets delivered to mcplayhd: the classifier service and the generated client.

## setup (venv)

```sh
python -m venv .venv
# TODO: activate + pip install -r requirements.txt
# TODO: copy the model files into models/ (see models/README.md)
```

## run

```sh
uvicorn api.main:app   # TODO: host/port for the server
```

Docs: `/docs` · spec: `/openapi.json`

## TODO
- endpoints & what the numbers mean (handbook)
- generating the java client (`scripts/generate_client.sh`)
