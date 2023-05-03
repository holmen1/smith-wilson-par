from typing import Dict, Any, List

from fastapi import FastAPI, Response, status
import numpy as np
from pydantic import BaseModel
from .smithwilson import RiskFreeRates


class RequestModel(BaseModel):
    par_rates: list[float]
    par_maturities: list[int]
    projection: list[int]
    ufr: float
    convergence_maturity: int
    tol: float
    alpha0: float | None

class ResponseModel(BaseModel):
    alpha: float
    rfr: list[float]


app = FastAPI(
    title="smith-wilson-par",
    description="A RESTful API to extrapolate Risk Free Rates from par swap rates using the Smith-Wilson method",
    version="1.5.1",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/rfr/api/rates/", status_code=200)
async def create_rates(swinput: RequestModel, response: Response) -> ResponseModel:
    rates = np.array(swinput.par_rates)
    maturities = np.array(swinput.par_maturities)
    projection = np.arange(swinput.projection[0], swinput.projection[1])
    ufr = swinput.ufr
    alpha0 = swinput.alpha0
    convergence_maturity = swinput.convergence_maturity
    tol = swinput.tol

    RFR = RiskFreeRates(rates, maturities, projection, ufr, convergence_maturity, tol, alpha0)
    alpha, r = RFR.result
    if rfr := list(r):
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(alpha=alpha, rfr=rfr)