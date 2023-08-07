# smith-wilson-par

## Description
 
A RESTful API to extrapolate Risk Free Rates from par swap rates using
the Smith-Wilson method.


See [EIOPA Risk Free Rate Technical Documentation](https://www.eiopa.europa.eu/system/files/2022-12/eiopa-bos-2022-547-new-rfr-technical-documentation.pdf)

## Usage

## API

sw_parameters.json
```json
{
  "par_rates": [0.03495, 0.0324, 0.0298, 0.02855],
  "par_maturities": [2, 3, 5, 10],
  "projection": [1, 151],
  "ufr": 0.0345,
  "convergence_maturity": 20,
  "tol": 1E-4
}
```


```bash
uvicorn api.main:app
INFO:     Started server process [9354]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
````

```bash
curl -X POST 'http://127.0.0.1:8000/rfr/api/rates' -H 'accept: application/json' -H 'Content-Type: application/json' -d @./Data/sw_parameters.json
```

```json
{"alpha":0.39922635774331505,"rfr":[0.035834839761121895,0.03401966679727653,0.031544539162605245,..., 0.03392432779538157,0.03392816454917802],"price":[1.0,0.9949057833655796,0.9898401220563251,0.984810806107...]}
```

Rate projection with predefined alpha
```bash
curl -X POST 'http://127.0.0.1:8000/rfr/api/rates?alpha0=0.17' -H 'accept: application/json' -H 'Content-Type: application/json' -d @./Data/sw_parameters.json
```

## Dockerized API

Build
```bash
docker build --tag 'smith-wilson-api' .
```
Run
```bash
docker run -dp 8004:8000 'smith-wilson-api'
```
Test
```bash
curl 'http://localhost:8004'
```
```json
{"message":"Hello, World!"}
```
Stop
```bash
docker ps
```
```bash
CONTAINER ID  IMAGE  COMMAND CREATED  STATUS  PORTS NAMES  
399836b60511    holmen1/smith-wilson-api  "uvicorn api.main:ap…"  About a minute ago   Up About a minute  0.0.0.0:8004->8000/tcp, :::8004->8000/tcp unruffled_dewdney
```

```bash
docker stop unruffled_dewdney
```

Prune
```bash
$ docker image prune
```

## Deploy to Azure Container Instances

```bash
RESOURCE_GROUP="actuarial-apps-rg"
LOCATION="northeurope"
API_NAME="smith-wilson-api"
GITHUB_USERNAME="holmen1"
ACI_NAME="aci"$GITHUB_USERNAME
```

```bash
docker build --tag $GITHUB_USERNAME/$API_NAME .  
docker push $GITHUB_USERNAME/$API_NAME
```

Create a resource group
```bash
az group create --name $RESOURCE_GROUP --location $LOCATION
```

Create a container
```bash
az container create \
  --name $ACI_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $GITHUB_USERNAME/$API_NAME \
  --ports 8000 \
  --environment-variables 'PORT'='8000' \
  --dns-name-label $ACI_NAME
```

```bash
az container show --resource-group $RESOURCE_GROUP --name $ACI_NAME --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" --out table
````
FQDN  ProvisioningState  
aciholmen1.northeurope.azurecontainer.io  Succeeded

```bash
curl -X POST 'aciholmen1.northeurope.azurecontainer.io:8000/rfr/api/rates' -H 'acceptn/json' -H 'Content-Type: application/json' -d @./Data/sw_parameters.json
```


Pull the container logs
```bash
az container logs --resource-group $RESOURCE_GROUP --name $ACI_NAME
```
INFO:     Started server process [19]  
INFO:     Waiting for application startup.  
INFO:     Application startup complete.  
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)  
INFO:     10.92.0.24:57618 - "GET / HTTP/1.1" 200 OK  
INFO:     10.92.0.24:51326 - "POST /rfr/api/rates HTTP/1.1" 201 Created
INFO:     10.92.0.25:50880 - "GET /openapi.json HTTP/1.1" 200 OK


Clean up resources
```bash
az group delete --name $RESOURCE_GROUP
```

### Notebook
[demo.ipynb](https://github.com/holmen1/smith-wilson-par/blob/master/smith-wilson-par/demo.ipynb)


## TODO

* [x] Robust find_alpha
* [x] Deploy to Azure
* [ ] Add tests
* [ ] RequestModel parameter validation
* [ ] Zero coupon bond
* [ ] Add documentation
* [ ] Add logging
* [ ] Add GitHub Actions
* [x] Add Dockerfile
* [x] Add Docker-compose
