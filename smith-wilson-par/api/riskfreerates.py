"""
Created August 2023
"""
__author__ = 'holmen1'

import numpy as np
from scipy import interpolate
from api.smithwilson import SmithWilson


class RiskFreeRates(object):

    def __init__(self, swap_rates, sw_maturities, maturities, ufr, convergence_t, tol, cra, alpha0):
        """
        swap_rates: array of swap par rates
        sw_maturities: maturities of swap rates
        maturities: maturities to project
        """
        self.par_adjusted = swap_rates - cra
        self.sw_maturities = sw_maturities
        self.maturities = maturities

        self.SW = SmithWilson(ufr, convergence_t, tol, alpha0)

    def yearly(self):
        alpha, price = self.SW.project(self.par_adjusted, self.sw_maturities, self.maturities)
        r = rate(price, self.maturities)
        return (alpha, price, r)

    def monthly(self):
        """
        Interpolate the yearly rates to monthly rates
        """
        alpha, price = self.SW.project(self.par_adjusted, self.sw_maturities, self.maturities)

        # Add values for year 0
        years = np.insert(self.maturities, 0, 0)
        prices = np.insert(price, 0, 1.0)

        # Interpolate monthly prices with cubic spline
        f = interpolate.interp1d(years * 12, prices, kind='cubic')
        months = np.arange(years[0] * 12, years[-1] * 12 + 1)
        monthly_prices = f(months)

        # Calculate monthly rates, letting the r[0] <- r[1/12]
        t = months / 12
        r = rate(monthly_prices[1:], t[1:])
        r = np.insert(r, 0, r[0])
        return (alpha, monthly_prices, r)


def rate(p, t):
    return np.power(1 / p, 1 / t) - 1
