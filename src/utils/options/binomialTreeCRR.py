import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class BinomialTreeCRR:

    def __init__(self, T: float, N: int, sigma: float, r: float, S: float, K: float,  option_type: str, american_option: bool = False):
        self.T = T                              # Time to expiration
        self.N = N                              # noqa # Number of intervals -> See calculation of newtonRhapson in volatility
        self.delta_t = None                     # Time step
        self.sigma = sigma                      # Volatility
        self.r = r                              # Risk-free rate
        self.S = S                              # Current stock price
        self.K = K                              # Strike price
        self.u = None                           # Up factor
        self.d = None                           # Down factor
        self.p = None                           # Risk-neutral probability of up movement

        # Type of option (Call C or Put P)
        self.option_type = option_type
        self.american_option = american_option  # noqa # Bool Parameter if the option is American or European

    def calculate_delta_t(self) -> None:
        self.delta_t = self.T / self.N

    def calculate_up_factor(self) -> None:
        self.u = np.exp(self.sigma * np.sqrt(self.delta_t))

    def calculate_down_factor(self) -> None:
        self.d = np.exp(-self.sigma * np.sqrt(self.delta_t))

    def calculate_payoff(self) -> float:
        self.payoff = np.maximum(
            self.S - self.K, 0) if option_type == "C" else np.maximum(-self.S + self.K, 0)

    def calculate_risk_neutral_prob(self) -> None:
        self.p = (np.expo(self.r * self.delta_t) - self.d) / (self.u - self.d)

    def terminal_payoffs(self) -> float:
        payoffs = []
        for i in range(self.N + 1):
            asset_price = self.S * (self.u ** i) * (self.N - i)
            payoffs.append(max(asset_price - self.K, 0)
                           if self.option_type == "C" else max(self.K - asset_price, 0))
        return payoffs

    def run_calculation(self):
        self.calculate_delta_t()
        self.calculate_up_factor()
        self.calculate_down_factor()
        self.calculate_risk_neutral_prob()

        option_values = self.terminal_payoff(self.american_option)
