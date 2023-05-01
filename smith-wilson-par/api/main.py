from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel
from .smithwilson import RiskFreeRates


class SWinput(BaseModel):
    par_rates: list[float]
    par_maturities: list[int]
    projection: list[int]
    ufr: float
    alpha0: float
    convergence_maturity: int
    tol: float


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/rfr/api/{alpha}")
async def read_alpha(alpha: float):
    return {"message": f"alpha {alpha}"}

# Retrive SWinput
@app.post("/rfr/api/rates/")
async def read_rates(swinput: SWinput):
    rates = np.array(swinput.par_rates)
    maturities = np.array(swinput.par_maturities)
    projection = np.arange(swinput.projection[0], swinput.projection[1])
    ufr = swinput.ufr
    alpha0 = swinput.alpha0
    convergence_maturity = swinput.convergence_maturity
    tol = swinput.tol

    RFR = RiskFreeRates(rates, maturities, projection, ufr, convergence_maturity, tol)
    alpha, r = RFR.result

    return {"r[0]": r[0], "r[9]": r[9], "alpha": alpha}