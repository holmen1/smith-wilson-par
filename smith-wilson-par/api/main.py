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


@app.post("/rfr/api/rates", status_code=200)
async def create_rates(req: RequestModel, response: Response, alpha0: float | None = None) -> ResponseModel:
    rates = np.array(req.par_rates)
    maturities = np.array(req.par_maturities)
    start_year = req.projection[0]
    end_year = req.projection[1]  # not inclusive
    intervals_per_year = req.projection[2] if len(req.projection) == 3 else 1
    projection = np.arange(start_year, end_year, 1 / intervals_per_year).round(6)  # rounding to ensure integer years
    ufr = req.ufr
    convergence_maturity = req.convergence_maturity
    tol = req.tol

    RFR = RiskFreeRates(rates, maturities, projection, ufr, convergence_maturity, tol, alpha0)
    alpha, r, price = RFR.result
    if rfr := list(r):
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(alpha=alpha, rfr=rfr, price=list(price))
