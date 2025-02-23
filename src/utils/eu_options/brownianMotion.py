import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

class BrownianMotion:
    def __init__(self, k: int, n: int):
        self.B = [0]
        self.k = k
        self.n = n
        self.T: list[list[float]] = []
        
    def simulate(self):
        for _ in range(self.n):
            self.B = [0]
            for _ in range(self.k):
                self.B.append(
                    self.B[-1] + np.random.normal(0, 1)
                )
            plt.plot(self.B)
        
    def get_B(self):
        return self.B
    
    def get_T(self):
        return self.T
        
    def plot(self):
        plt.show()
        
bm = BrownianMotion(251, 1000)
bm.simulate() 
