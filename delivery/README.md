# GRL replay classifier

Everything that gets delivered to mcplayhd: the classifier service and the generated Java client.

The service puts FastBuilder replays into clusters of similar replays. Every cluster is described by the hand-labeled replays in it (which techniques were used, how suspicious they looked), so a new replay's cluster tells you what it most likely is.

## setup (venv)

Needs Python 3.12 (tested with 3.12.10). From the `delivery` folder:

```sh
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then put the model bundle into `models/` as `model_bundle.joblib` (see `models/README.md`). The versions in `requirements.txt` are pinned on purpose: the bundle only loads with the scikit-learn version it was saved with.

## run

From the `delivery` folder, with the venv active:

```sh
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

- `--host 127.0.0.1`: only reachable from the same machine. Use `--host 0.0.0.0` if the caller runs on another machine or the server runs inside Docker.
- `--port 8000`: any free port works; the client just has to use the same one.
- While developing, add `--reload` to restart on every file save. Leave it out in production.

The model is loaded on the first request (under a second), not at startup. To switch to another model, replace `models/model_bundle.joblib` and restart the server.

Interactive docs: `/docs` · machine-readable spec: `/openapi.json`

## batch size

`POST /label` takes a list of replays. Replays are big (about 70 KB of JSON each, so 300 replays are about 20 MB), and the classification itself is fast (1000 replays in about 5 s). Send large amounts in **chunks of a few hundred replays** instead of one huge request, so a single request doesn't get too large or slow.

## handbook

### versions

- `model_version` (e.g. `v3_noclicks`) is in every response. It changes when the model is retrained or relabeled. **Cluster ids only mean something together with their model version**: `NORMAL_3` of one model has nothing to do with `NORMAL_3` of the next one.
- The API version (e.g. `1.0.0`, shown in `/docs` and in the Java client) changes when endpoints or response shapes change. Then the Java client has to be regenerated.

### endpoints

| endpoint | what it returns |
|---|---|
| `POST /label` | the cluster of each replay you send |
| `GET /clusters` | the description of every cluster (cache it, it only changes with `model_version`) |
| `GET /techniques` | all technique names that can appear in `/clusters` |
| `GET /suspicious_levels` | the four suspicion levels, in order |
| `GET /version` | only the `model_version` |

### POST /label

Input: a list of replays in the same JSON format as the thesis data. Only these fields are used, everything else is ignored:

- `idAnonymous`, `fastBuilderMode` (`EXTRASHORT`, `SHORT`, `NORMAL`, `LONG`, `ONESTACK`, `INCLINED`, `INCLINEDSHORT`)
- `stepData`: one entry per tick with `playerPosition` (`x, y, z, yaw, pitch`), `sneaking`, `clicks` and `blocksChanged` (`material`, `loc` with `x, y, z`)

Output: one result per replay, **in the same order as sent**:

- `id`: the `idAnonymous` you sent
- `cluster`: e.g. `EXTRASHORT_1`, the key into `/clusters`
- `confidence`: 0–1, the share of the 15 most similar training replays that are in this cluster. 1.0 means all of them agree; low values mean the replay sits between clusters.

`cluster` and `confidence` are `null` when a replay can't be classified: the model looks at a 50-tick window of building, so replays that place no block or are too short for such a window are skipped.

### GET /clusters

Per cluster:

- `cluster_labels`: the techniques of the hand-labeled replays in this cluster, as `share` = the share of those replays that used it, highest first. One replay can use several techniques, so the shares can add up to more than 1. Replays labeled as autoclicker count in the total, but "autoclicker" itself is not listed (clicks are not used by the model).
- `suspicious_levels`: how many hand-labeled replays in this cluster got each suspicion level. All four levels are always listed, with 0 where nobody voted. Autoclicker replays are left out here.

A cluster without any hand-labeled replays has an empty `cluster_labels` and all counts at 0. That means "no information", not "legit".

### techniques

| name | meaning |
|---|---|
| `sneak` | sneak bridge |
| `ninja` | ninja bridge |
| `noshift` | noshift staircase |
| `telly` | telly bridge |
| `breezily` | breezily bridge |
| `moon` | moonwalk |
| `god` | god bridge |
| `tower` | towering |
| `0cps` | 0cps bridge |
| `stair` | onestack-shaped (staircase) building |
| `noob` | something weird / unusual building |
| `unclear` | a technique that can't be clearly identified as a known one |
| `cheats` | the building comes from cheats |
| `bug` | the replay looks caused by a bug |

### suspicion levels

`legit` (0), `maybe` (1), `suspicious` (2), `blatant` (3), from the hand labels.

## Java client

The ready-made client is in `client/java` (a Maven project, Gradle files included). It uses Java's built-in HTTP client (Java 11+) and Jackson.

```java
ApiClient client = new ApiClient();
client.updateBaseUri("http://localhost:8000");
ClassifierApi api = new ClassifierApi(client);

LabelResponse response = api.label(replays);       // List<Replay>
String cluster = response.getResults().get(0).getCluster();   // e.g. "EXTRASHORT_1", or null
ClustersResponse clusters = api.getClusters();     // cache per model_version
```

To regenerate it (after the API version changed), start the server and run from the `delivery` folder:

```sh
sh scripts/generate_client.sh                      # or: sh scripts/generate_client.sh http://host:port
```

The script uses the `openapitools/openapi-generator-cli` Docker image. Without Docker, the same generator exists as a jar (`java -jar openapi-generator-cli.jar generate ...`, same options as in the script).
