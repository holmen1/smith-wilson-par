# smith-wilson-par

## Description
 
A RESTful API to extrapolate Risk Free Rates from par swap rates using
the Smith-Wilson method.


See [EIOPA Risk Free Rate Technical Documentation](https://www.eiopa.europa.eu/system/files/2022-12/eiopa-bos-2022-547-new-rfr-technical-documentation.pdf)

## Usage

### API

sw_parameters.json
```json
{
  "par_rates": [0.03495, 0.0324, 0.0298, 0.02855],
  "par_maturities": [2, 3, 5, 10],
  "projection": [1, 151],
  "ufr": 0.0345,
  "convergence_maturity": 20,
  "tol": 1E-4,
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
curl -X POST 'http://127.0.0.1:8000/rfr/api/rates/' -H 'accept: application/json' -H 'Content-Type: application/json' -d @./Data/sw_parameters.json
```

```json
{"alpha":0.39922635774331505,"rfr":[0.035834839761121895,0.03401966679727653,0.031544539162605245,0.029971503918941877,0.028975600564583148,0.028254908097557152,[...], 0.03392432779538157,0.03392816454917802]}
```

Rate projection with predefined alpha
```bash
curl -X POST 'http://127.0.0.1:8000/rfr/api/rates?alpha0=0.17' -H 'accept: application/json' -H 'Content-Type: application/json' -d @./Data/sw_parameters.json
```

### Dockerized API


Create
```bash
$ docker compose build

$ docker compose up -d

[+] Running 1/1
 ⠿ Container smith-wilson-par_web_1  Started  
```
Test
```bash
$ curl 'http://localhost:8004'

{"message":"Hello, World!"}
```
Destroy
```bash
$ docker compose down

[+] Running 2/2
 ⠿ Container smith-wilson-par_web_1    Removed                                                                                                                    0.8s
 ⠿ Network "smith-wilson-par_default"  Removed
 ```
  Prune
```bash
$ docker image prune
```

### Notebook
[demo.ipynb](https://github.com/holmen1/smith-wilson-par/blob/master/smith-wilson-par/demo.ipynb)


## TODO

* [x] Robust find_alpha
* [ ] Publish to Azure
* [ ] Add tests
* [ ] RequestModel parameter validation
* [ ] Add documentation
* [ ] Add logging
* [ ] Add CI/CD
* [x] Add Dockerfile
* [x] Add Docker-compose
