#!/bin/bash

API_NAME="smith-wilson-api"
GITHUB_USERNAME="holmen1"
TAG=${1:-latest}

docker build --tag $GITHUB_USERNAME/$API_NAME:$TAG smith-wilson-par/

docker push $GITHUB_USERNAME/$API_NAME:$TAG
