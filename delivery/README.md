# GRL replay classifier

Everything that gets delivered to McPlayHD: the classifier service and the generated Java client.

The service puts FastBuilder replays into clusters of similar replays. Clusters are described by (1200+) hand-labeled replays combined with a voting logic to scale the labels over the full training data. New replays are classified regarding which bridging technique was most likely used and how suspicious similar replays were.

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
- `--reload` to restart on every file save (use in development only)

The model is loaded on the first request (under a second), not at startup. To switch to another model, replace `models/model_bundle.joblib` and restart the server.

Interactive docs: `/docs` · machine-readable spec: `/openapi.json`

## batch size

`POST /label` takes a list of replays. In development, replays were about 70 KB of JSON per replay (ca 20 MB for 300 replays) and classification itself was fast (~5s for 1000 replays). Recommendation is to send larger amounts of data in **chunks of a few hundred replays**.

## handbook

### versions

- `model_version` (e.g. `v3_noclicks`) is in every response. It changes when the model is retrained or relabeled. **Cluster ids only mean something together with their model version**: `NORMAL_3` of one model has nothing to do with `NORMAL_3` of the next one.
- The API version (e.g. `1.0.0`, shown in `/docs` and in the Java client) changes when endpoints or response shapes change. Then the Java client has to be regenerated.

### endpoints

| endpoint | what it returns                                                                 |
|---|---------------------------------------------------------------------------------|
| `POST /label` | the calculated cluster of each replay you send                                  |
| `GET /clusters` | the description of every cluster (cacheable, only changes with `model_version`) |
| `GET /techniques` | all technique names that can appear in `/clusters`                              |
| `GET /suspicious_levels` | all suspicion levels that can appear in `/clusters`                             |
| `GET /version` | the `model_version`                                                             |

### POST /label

Input: a list of replays in the same JSON format as the thesis data. Only these fields are used, everything else is ignored:

- `idAnonymous`
- `fastBuilderMode` (`EXTRASHORT`, `SHORT`, `NORMAL`, `LONG`, `ONESTACK`, `INCLINED`, `INCLINEDSHORT`)
- `stepData`  (one entry per tick with) 
  - `playerPosition`
    - `x`
    - `y`
    - `z`
    - `yaw`
    - `pitch` 
  - `sneaking`
  - `clicks` 
  - `blocksChanged`
    - `material` 
    - `loc` 
      - `x` 
      - `y` 
      - `z`

All of these fields are required. If even one replay in the list misses a field or has a wrong type, the **whole request** is rejected with HTTP 422 (the response says which replay and field), and no replay gets classified.

Output: one result per replay, **in the same order as sent**:

- `id`: the `idAnonymous` you sent
- `cluster`: e.g. `EXTRASHORT_1`, key for `/clusters`
- `confidence`: 0–1, the share of the 15 most similar training replays that are in this cluster. 1.0 means all of them agree; low values mean the replay sits between clusters.

`cluster` and `confidence` are `null` when a replay can't be classified:
- the model looks at a 50-tick window of building, so replays that place no block or are too short for such a window are skipped
- the `fastBuilderMode` is not one the model was trained on (e.g. a new mode)

### GET /clusters

Per cluster:

- `cluster_labels`: the techniques of the hand-labeled replays in this cluster, as `share` = the share of those replays that used it, highest first. One replay can use several techniques, so the shares can add up to more than 1. Replays labeled as autoclicker count in the total, but "autoclicker" itself is not listed (clicks are not used by the model).
- `suspicious_levels`: how many hand-labeled replays in this cluster got each suspicion level. All four levels are always listed, with 0 where nobody voted. Autoclicker replays are left out here.

A cluster without any hand-labeled replays has an empty `cluster_labels` and all counts at 0. That means "no information", not "legit".

### techniques
_from hand-labeling_

| name | meaning                                                                                                     |
|---|-------------------------------------------------------------------------------------------------------------|
| `sneak` | sneak bridge                                                                                                |
| `ninja` | ninja bridge                                                                                                |
| `noshift` | noshift staircase                                                                                           |
| `telly` | telly bridge                                                                                                |
| `breezily` | breezily bridge                                                                                             |
| `moon` | moonwalk                                                                                                    |
| `god` | god bridge                                                                                                  |
| `tower` | extensive towering <br> (doesn't include small tower before the finish island etc)                          |
| `0cps` | 0cps bridge (all variations)                                                                                |
| `stair` | onestack-shaped bridging, usually combined with other techniques <br> (e.g. ninja + stair = ninja onestack) |
| `noob` | weird, particular or non-bridging behavior <br> (e.g. not bridging towards the goal, building a house etc)  |
| `unclear` | looks like real bridging techniques, but can't clearly be labeled as one                                    |
| `cheats` | bridging behavior / shape that is caused by cheats                                                          |
| `bug` | replay includes bugs that impact the bridging behavior / shape                                              |

### suspicion levels
_from hand-labeling_

- `legit` (0): looks legit
- `maybe` (1): looks legit, but some suspicious patterns are present
- `suspicious` (2): looks like cheats, but not 100% sure
- `blatant` (3): clearly cheating (or behavior that reproduces clear cheating patterns)

#### autoclicker note
_The original set of hand-labeled data includes a technique label for autoclicker (similar to `cheats`). Later models specifically should not consider clicking patterns, therefore those autoclicker labels were removed and their suspicious levels ignored. Replays affected by this do not have a suspicious level anymore, which is the reason why some clusters have fewer suspicion level votes._ 

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

The script uses the `openapitools/openapi-generator-cli` Docker image. Without Docker, the same generator exists as a jar (needs Java 11+). With the server running, from the `delivery` folder:

```sh
curl -f -o openapi.json http://localhost:8000/openapi.json
curl -fL -o openapi-generator-cli.jar https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.27.0/openapi-generator-cli-7.27.0.jar
rm -rf client/java
java -jar openapi-generator-cli.jar generate \
    -i openapi.json \
    -g java \
    --library native \
    -o client/java \
    --type-mappings=number=Double \
    --additional-properties=groupId=grl,artifactId=grl-replay-classifier-client,artifactVersion=1.0.0,invokerPackage=grl.client,apiPackage=grl.client.api,modelPackage=grl.client.model,openApiNullable=false,hideGenerationTimestamp=true
```

Set `artifactVersion` to the API version shown in `/docs` (the script reads it from `openapi.json` by itself).
