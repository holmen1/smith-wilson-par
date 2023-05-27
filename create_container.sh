#!/bin/bash

RESOURCE_GROUP="actuarial-apps-rg"
LOCATION="northeurope"
API_NAME="smith-wilson-api"
GITHUB_USERNAME="holmen1"
ACI_NAME="aci"$GITHUB_USERNAME

## Create a resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

## Create a container group
az container create \
  --name $ACI_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $GITHUB_USERNAME/$API_NAME \
  --ports 80 \
  --environment-variables 'PORT'='8000' \
  --dns-name-label $ACI_NAME
