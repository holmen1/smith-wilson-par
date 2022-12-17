"""

Created December 2022

@author: holmen1

"""

import numpy as np


class RiskFreeRates(object):
    def __init__(self, swap_rates, swap_maturities, maturities, ufr):
        alpha = 0.1
        omega = np.log(1 + ufr)
        self.maturities = maturities

        p = np.ones(swap_maturities.size)
        C = self.cashflows(swap_rates, swap_maturities, maturities)
        d = np.exp(-omega * maturities)
        q = C.T @ d
        Q = np.diag(d) @ C
        H = self.heart(maturities, maturities, alpha)
        b = np.linalg.solve(Q.T @ H @ Q, p - q)

        self.price = d + np.diag(d) @ H @ Q @ b

    def rates(self):
        return np.power(1 / self.price, 1 / self.maturities) - 1

    def heart(self, u, v, alpha):
        u_mat = np.tile(u, [v.size, 1]).transpose()
        v_mat = np.tile(v, [u.size, 1])
        return 0.5 * (alpha * (u_mat + v_mat) + np.exp(-alpha * (u_mat + v_mat)) - alpha * np.absolute(
            u_mat - v_mat) - np.exp(-alpha * np.absolute(u_mat - v_mat)))

    def cashflows(self, rates, maturities, durations):
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
