# smith-wilson-par

## Description
 
A RESTful API to extrapolate Risk Free Rates from par swap rates using
the Smith-Wilson method.


See [EIOPA Risk Free Rate Technical Documentation](https://www.eiopa.europa.eu/system/files/2022-12/eiopa-bos-2022-547-new-rfr-technical-documentation.pdf)

## Usage

### API

```bash
uvicorn api.main:app
INFO:     Started server process [9354]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
````

```bash
curl -X POST 'http://127.0.0.1:8000/rfr/api/rates/' -H 'accept: application/json' -H 'Content-Type: application/json' -d @./Data/sw_parameters.json

{"r[0]":0.035834839761121895,"r[9]":0.027357998563122488,"alpha":0.39922635774331505}
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
[demo.ipynb](https://github.com/holmen1/smith-wilson-par/blob/master/demo.ipynb)


## TODO

* [ ] Robust find_alpha
* [ ] Publish to Azure
* [ ] Add tests
* [ ] Add documentation
* [ ] Add logging
* [ ] Add CI/CD
* [x] Add Dockerfile
* [x] Add Docker-compose
