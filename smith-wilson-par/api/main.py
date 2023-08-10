from typing import Dict, Any, List

from fastapi import FastAPI, Response, status
import numpy as np
from omegaconf import OmegaConf
from pydantic import BaseModel
from .riskfreerates import RiskFreeRates

# Load the configuration file
config = OmegaConf.load("./conf/config.yaml")


class RequestModel(BaseModel):
    par_rates: list[float]
    par_maturities: list[int]


class ResponseModel(BaseModel):
    alpha: float
    rfr: list[float]
    price: list[float]


app = FastAPI(
    title="smith-wilson-par",
    description="A RESTful API to extrapolate Risk Free Rates from par swap rates using the Smith-Wilson method",
    version="1.5.1",
)


@app.get("/")
async def root():
    return {"message": "Hello from Smith-Wilson API!"}


@app.post("/api/eiopa", status_code=200)
async def create_eiopa_rates(req: RequestModel, response: Response) -> ResponseModel:
    rates = np.array(req.par_rates)
    maturities = np.array(req.par_maturities)

    RFR = RiskFreeRates(config, "sek")
    alpha, price, rates = RFR.yearly(rates, maturities)
    if a := alpha:
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(alpha=a, rfr=list(rates), price=list(price))


@app.post("/api/monthly", status_code=200)
async def create_monthly_rates(req: RequestModel, response: Response) -> ResponseModel:
    rates = np.array(req.par_rates)
    maturities = np.array(req.par_maturities)

    RFR = RiskFreeRates(config, "sek")
    alpha, price, rates = RFR.monthly(rates, maturities)

    if a := alpha:
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(alpha=a, rfr=list(rates), price=list(price))
