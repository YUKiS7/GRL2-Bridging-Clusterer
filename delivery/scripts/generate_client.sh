#!/bin/sh
# generates the java client from the running api's openapi spec
#
# run from the delivery folder while the server is running:
#   sh scripts/generate_client.sh [server url]
# output: client/java (a maven project), regenerate it whenever API_VERSION changes
set -e

SERVER_URL="${1:-http://localhost:8000}"
OUT_DIR="client/java"

# 1. download the spec from the running server
curl -sf "$SERVER_URL/openapi.json" -o openapi.json

# the api version (settings.API_VERSION) becomes the version of the java artifact
API_VERSION=$(grep -o '"version":"[^"]*"' openapi.json | head -1 | cut -d'"' -f4)
echo "generating java client for api version $API_VERSION"

# docker needs a windows path when this runs in git bash, a normal path everywhere else
HOST_DIR=$(pwd -W 2>/dev/null || pwd)

# 2. generate. library "native" = java's built-in http client (java 11+), so the only extra dependency is jackson
#    number=Double: python floats become double instead of BigDecimal (positions, shares, confidence)
rm -rf "$OUT_DIR"
MSYS_NO_PATHCONV=1 docker run --rm -v "$HOST_DIR:/local" openapitools/openapi-generator-cli generate \
    -i /local/openapi.json \
    -g java \
    --library native \
    -o "/local/$OUT_DIR" \
    --type-mappings=number=Double \
    --additional-properties=groupId=grl,artifactId=grl-replay-classifier-client,artifactVersion="$API_VERSION",invokerPackage=grl.client,apiPackage=grl.client.api,modelPackage=grl.client.model,openApiNullable=false,hideGenerationTimestamp=true

echo "done: $OUT_DIR"
