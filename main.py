import numpy as np
from smithwilson import RiskFreeRates

rates = np.array([0.03405, 0.03164, 0.02914, 0.02753])
maturities = np.array([2, 3, 5, 10])
projection = np.arange(1, 151)
#projection = np.arange(1, 12)
ufr = 0.0345
alpha0 = 0.397593
convergence_maturity = 20
tol = 1e-4

RFR = RiskFreeRates(rates, maturities, projection, ufr, convergence_maturity, tol)
alpha, r = RFR.result
print(r[maturities-1])
print(f'alpha = {alpha}')
print(f'f_20 = {(1 + r[20])**21/(1 + r[19])**20 - 1}')