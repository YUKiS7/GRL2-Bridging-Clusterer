#!/bin/sh
# generates the java client from the running api's openapi spec
# TODO:
# 1. download http://localhost:8000/openapi.json to openapi.json
# 2. docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
#      -i /local/openapi.json -g java -o /local/client/java
