import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class BinomialTreeCRR:

    def __init__(self, T: float, N: int, sigma: float, r: float, S: float, K: float, option_type: str, american_option: bool = False):
        self.T = T                              # Time to expiration
        self.N = N                              # Number of intervals
        self.delta_t = None                     # Time step
        self.sigma = sigma                      # Volatility
        self.r = r                              # Risk-free rate
        self.S = S                              # Current stock price
        self.K = K                              # Strike price
        self.u = None                           # Up factor
        self.d = None                           # Down factor
        self.p = None                           # Risk-neutral probability

        # Option type: "C" for call, "P" for put
        self.option_type = option_type
        self.american_option = american_option

    def calculate_delta_t(self) -> None:
        self.delta_t = self.T / self.N

    def calculate_up_factor(self) -> None:
        self.u = np.exp(self.sigma * np.sqrt(self.delta_t))

    def calculate_down_factor(self) -> None:
        self.d = np.exp(-self.sigma * np.sqrt(self.delta_t))

    def calculate_payoff(self) -> float:
        self.payoff = np.maximum(
            self.S - self.K, 0) if self.option_type == "C" else np.maximum(self.K - self.S, 0)

    def calculate_risk_neutral_prob(self) -> None:
        self.p = (np.exp(self.r * self.delta_t) - self.d) / (self.u - self.d)

    def terminal_payoffs(self) -> list:
        payoffs = []
        for i in range(self.N + 1):
            asset_price = self.S * (self.u ** i) * (self.d ** (self.N - i))
            if self.option_type == "C":
                payoff = max(asset_price - self.K, 0)
            elif self.option_type == "P":
                payoff = max(self.K - asset_price, 0)
            payoffs.append(payoff)
        return payoffs

    def run_calculation(self) -> float:
        self.calculate_delta_t()
        self.calculate_up_factor()
        self.calculate_down_factor()
        self.calculate_risk_neutral_prob()

        option_values = self.terminal_payoffs()

        for step in range(self.N - 1, -1, -1):
            new_values = []
            for i in range(step + 1):

                asset_price = self.S * (self.u ** i) * (self.d ** (step - i))

                continuation_value = np.exp(-self.r * self.delta_t) * (
                    self.p * option_values[i + 1] +
                    (1 - self.p) * option_values[i]
                )
                if self.american_option:
                    if self.option_type == "C":
                        immediate_exercise = max(asset_price - self.K, 0)
                    else:
                        immediate_exercise = max(self.K - asset_price, 0)
                    new_value = max(continuation_value, immediate_exercise)
                else:
                    new_value = continuation_value
                new_values.append(new_value)
            option_values = new_values

        return option_values[0]

    def plot_tree(self) -> None:
        """
        Plots the CRR binomial tree with asset prices at each node.
        The x-axis represents time steps and the y-axis shows the asset price.
        """
        # Ensure the basic parameters are calculated
        self.calculate_delta_t()
        self.calculate_up_factor()
        self.calculate_down_factor()

        # Dictionary to hold node positions: keys are (level, index) and values are (x, y)
        nodes = {}
        levels = self.N + 1  # total levels in the tree

        # Compute the asset price at each node
        for level in range(levels):
            for i in range(level + 1):
                # The asset price at a node with i up moves and (level - i) down moves:
                asset_price = self.S * (self.u ** i) * (self.d ** (level - i))
                # We'll use the time step (level) as the x-coordinate and asset price as the y-coordinate
                nodes[(level, i)] = (level, asset_price)

        # Create the plot
        plt.figure(figsize=(8, 6))

        # Draw connecting lines between nodes
        for level in range(levels - 1):
            for i in range(level + 1):
                x_current, y_current = nodes[(level, i)]
                # Down move: same index at next level
                x_down, y_down = nodes[(level + 1, i)]
                # Up move: index + 1 at next level
                x_up, y_up = nodes[(level + 1, i + 1)]

                # Plot line from current node to down child
                plt.plot([x_current, x_down], [y_current, y_down], 'k-', lw=1)
                # Plot line from current node to up child
                plt.plot([x_current, x_up], [y_current, y_up], 'k-', lw=1)

        # Plot the nodes themselves
        for (level, i), (x, y) in nodes.items():
            plt.scatter(x, y, color='blue', zorder=5)
            # Annotate the node with the asset price
            plt.text(x, y, f'{y:.2f}', fontsize=8, ha='center', va='bottom')

        plt.title("CRR Binomial Tree")
        plt.xlabel("Time Step")
        plt.ylabel("Asset Price")
        plt.grid(True)
        plt.show()
