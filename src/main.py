from utils.options.binomialTreeCRR import BinomialTreeCRR

crr = BinomialTreeCRR(1, 3, 0.2, 0.05, 100, 100)
crr.run_calculation()
print(crr.__dict__)
