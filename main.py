import numpy as np
from smithwilson import RiskFreeRates

rates = np.array([0.032, 0.0308, 0.0288, 0.0271])
maturities = np.array([2, 3, 5, 10])
projection = np.arange(1, 121)
ufr = 0.0345
alpha = 0.414598

RFR = RiskFreeRates(rates, maturities, projection, ufr, alpha)
r = RFR.rates()
print(r[:19])