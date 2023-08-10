"""
Created August 2023
"""
__author__ = 'holmen1'

from omegaconf import DictConfig
import numpy as np
from scipy import interpolate
from api.smithwilson import SmithWilson


class RiskFreeRates(object):

    def __init__(self, cfg: DictConfig, currency: str):
        """
        :param cfg: The configuration file
        :param currency: key to the risk free rate configuration (e.g. "sek")
        """
        rfr_config = cfg.risk_free_rates[currency]

        self.SW = SmithWilson(ufr=rfr_config.ufr,
                              convergence_t=rfr_config.convergence_maturity,
                              tol=rfr_config.tol,
                              alpha0=None)

        start_year = rfr_config.projection[0]
        end_year = rfr_config.projection[1]  # not inclusive
        self.projection = np.arange(start_year, end_year)
        self.sw_maturities = np.array(rfr_config.par_maturities)
        self.cra = rfr_config.credit_risk_adjustment

    def yearly(self, swap_rates, swap_maturities):
        assert len(swap_rates) == len(swap_maturities)
        assert np.array_equal(swap_maturities, self.sw_maturities)

        par_adjusted = swap_rates - self.cra
        alpha, price = self.SW.project(par_adjusted, swap_maturities, self.projection)
        r = rate(price, self.projection)
        return (alpha, price, r)

    def monthly(self, swap_rates, swap_maturities):
        """
        Add year 0 to the projection and interpolate monthly prices with cubic spline
        """
        assert len(swap_rates) == len(swap_maturities)
        assert np.array_equal(swap_maturities, self.sw_maturities)

        par_adjusted = swap_rates - self.cra
        alpha, price = self.SW.project(par_adjusted, swap_maturities, self.projection)

        # Add values for year 0
        years = np.insert(self.projection, 0, 0)
        prices = np.insert(price, 0, 1.0)

        # Interpolate monthly prices
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
