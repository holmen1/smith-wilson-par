from typing import Dict, Any, List

from fastapi import FastAPI, Response, status
import numpy as np
from pydantic import BaseModel
from .riskfreerates import RiskFreeRates


class RequestModel(BaseModel):
    par_rates: list[float]
    par_maturities: list[int]
    projection: list[int]
    ufr: float
    convergence_maturity: int
    tol: float
    credit_risk_adjustment: float


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
    start_year = req.projection[0]
    end_year = req.projection[1]  # not inclusive
    projection = np.arange(start_year, end_year)
    ufr = req.ufr
    convergence_maturity = req.convergence_maturity
    tol = req.tol
    cra = req.credit_risk_adjustment

    RFR = RiskFreeRates(rates, maturities, projection, ufr, convergence_maturity, tol, cra, None)
    alpha, price, rates = RFR.yearly()
    if a:=alpha:
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(alpha=a, rfr=list(rates), price=list(price))


@app.post("/api/monthly", status_code=200)
async def create_monthly_rates(req: RequestModel, response: Response) -> ResponseModel:
    rates = np.array(req.par_rates)
    maturities = np.array(req.par_maturities)
    start_year = req.projection[0]
    end_year = req.projection[1]  # not inclusive
    projection = np.arange(start_year, end_year)
    ufr = req.ufr
    convergence_maturity = req.convergence_maturity
    tol = req.tol
    cra = req.credit_risk_adjustment

    RFR = RiskFreeRates(rates, maturities, projection, ufr, convergence_maturity, tol, cra, None)
    alpha, price, rates = RFR.monthly()

    if a:=alpha:
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(alpha=a, rfr=list(rates), price=list(price))
