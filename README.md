## Smith-Wilson method

EIOPA Risk Free Rate extrapolation from par swap rates

### API

```bash
curl -X POST 'http://127.0.0.1:8000/rfr/api/rates/' -H 'accept: application/json' -H 'Content-Type: application/json' -d @./Data/sw_parameters.json

{"r[0]":0.035834839761121895,"r[9]":0.027357998563122488,"alpha":0.39922635774331505}
```

## TODO

* [ ] Robust find_alpha
* [ ] Add tests
* [ ] Add documentation
* [ ] Add logging
* [ ] Add CI/CD
* [ ] Add Dockerfile
* [ ] Add Docker-compose
