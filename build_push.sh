#!/bin/bash

API_NAME="smith-wilson-api"
GITHUB_USERNAME="holmen1"

docker build --tag $GITHUB_USERNAME/$API_NAME smith-wilson-par/

docker push $GITHUB_USERNAME/$API_NAME
