"""

Created December 2022

@author: holmen1

"""

import numpy as np
from scipy import optimize


class RiskFreeRates(object):

    def __init__(self, swap_rates, swap_maturities, maturities, ufr, convergence_t, tol, alpha0):
        # Variables as in EIOPA's Technical documentation
        omega = np.log(1 + ufr)
        u = maturities  # projection
        v = swap_maturities
        p = np.ones(v.size)
        C = cashflows(swap_rates, v, u)
        d = np.exp(-omega * u)
        q = C.T @ d
        Q = np.diag(d) @ C
        alpha = find_alpha(convergence_t, u, Q, p, q, tol) if alpha0 is None else alpha0
        H = heart(u, u, alpha)
        b = np.linalg.solve(Q.T @ H @ Q, p - q)

        price = d + np.diag(d) @ H @ Q @ b
        rates = np.power(1 / price, 1 / u) - 1
        self.result = (alpha, rates)


def heart(u, v, alpha):
    u_mat = np.tile(u, [v.size, 1]).T
    v_mat = np.tile(v, [u.size, 1])
    return 0.5 * (alpha * (u_mat + v_mat) + np.exp(-alpha * (u_mat + v_mat)) - alpha * np.absolute(
        u_mat - v_mat) - np.exp(-alpha * np.absolute(u_mat - v_mat)))


def cashflows(rates, maturities, durations):
    CT = np.zeros((maturities.size, durations.size))
    for i in np.arange(maturities.size):
        maturity_index = np.where(durations == maturities[i])[0]
        for j in np.arange(durations.size):
            if j < maturity_index:
                CT[i, j] = rates[i]
            elif j == maturity_index:
                CT[i, j] = 1 + rates[i]
            else:
                CT[i, j] = 0
    return CT.T  # = C


def find_alpha(t, u, Q, p, q, tol):
    alpha0 = 1E-3
    f = lambda a: gap(t, a, u, Q, p, q) - tol
    try:
        result = optimize.root_scalar(f, bracket=[alpha0, 1.2], method='brentq')
        alpha = result.root
    except:
        error = 1
        step = 1E-5
        while error > tol:
            error = f(alpha)
            alpha += step
    return alpha


def gap(t, alpha, u, Q, p, q):
    H = heart(u, u, alpha)
    b = np.linalg.solve(Q.T @ H @ Q, p - q)
    kappa = (1 + alpha * u @ Q @ b) / (np.sinh(alpha * u) @ Q @ b)
    return alpha / np.abs(1 - kappa * np.exp(alpha * t))
