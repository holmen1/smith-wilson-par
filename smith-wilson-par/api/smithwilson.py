"""
Created December 2022
"""
__author__ = 'holmen1'

import numpy as np
from scipy import optimize

# Constants useed in optimization
ALPHA_LOWER_BOUND = 1E-3
ALPHA_UPPER_BOUND = 1.2
STEP_SIZE = 1E-5

class SmithWilson(object):

    def __init__(self, ufr, convergence_t, tol, alpha0):
        self.ufr = ufr
        self.convergence_t = convergence_t
        self.tol = tol
        self.alpha0 = alpha0

    def project(self, swap_rates, swap_maturities, maturities):
        # Variables as in EIOPA's Technical documentation
        omega = np.log(1 + self.ufr)
        u = maturities  # projection
        v = swap_maturities
        p = np.ones(v.size)
        C = cashflows(swap_rates, v, u)
        d = np.exp(-omega * u)
        q = C.T @ d
        Q = np.diag(d) @ C
        alpha = find_alpha(self.convergence_t, u, Q, p, q, self.tol) if self.alpha0 is None else self.alpha0
        H = heart(u, u, alpha)
        b = np.linalg.solve(Q.T @ H @ Q, p - q)

        price = d + np.diag(d) @ H @ Q @ b
        return (alpha, price)


def heart(u, v, alpha):
    u_mat = np.tile(u, [v.size, 1]).T
    v_mat = np.tile(v, [u.size, 1])
    return 0.5 * (alpha * (u_mat + v_mat) + np.exp(-alpha * (u_mat + v_mat)) - alpha * np.absolute(
        u_mat - v_mat) - np.exp(-alpha * np.absolute(u_mat - v_mat)))


def cashflows(rates, maturities, durations):
    CT = np.zeros((maturities.size, durations.size))
    for i in np.arange(maturities.size):
        # Yearly settlement frequency
        settlement_indices = [c for c, x in enumerate(durations) if x <= maturities[i] and x % 1 == 0]
        for j in settlement_indices:
            CT[i, j] = rates[i]
        # Notional repayment
        CT[i, settlement_indices[-1]] += 1
    return CT.T  # = C


def find_alpha(t, u, Q, p, q, tol):
    """
    :return: alpha, giving a forward rate within tol from UFR at time t
    """
    alpha = ALPHA_LOWER_BOUND
    f = lambda a: gap(t, a, u, Q, p, q) - tol
    try:
        result = optimize.root_scalar(f, bracket=[alpha, ALPHA_UPPER_BOUND], method='brentq')
        alpha = result.root
    except Exception as e:
        print(f"Failed to optimize alpha value due to: {str(e)}.")
        # If optimization fails, do a simple search until tol is met
        error = 1
        step = STEP_SIZE
        while error > tol:
            error = f(alpha)
            alpha += step
    return alpha


def gap(t, alpha, u, Q, p, q):
    H = heart(u, u, alpha)
    b = np.linalg.solve(Q.T @ H @ Q, p - q)
    kappa = (1 + alpha * u @ Q @ b) / (np.sinh(alpha * u) @ Q @ b)
    return alpha / np.abs(1 - kappa * np.exp(alpha * t))
