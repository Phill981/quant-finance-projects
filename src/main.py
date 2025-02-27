from utils.options.binomialTreeCRR import BinomialTreeCRR

if __name__ == "__main__":
    # Create a CRR model with a small number of steps to keep the tree simple
    crr = BinomialTreeCRR(1, 3, 0.2, 0.05, 100, 100,
                          option_type="C", american_option=False)
    price = crr.run_calculation()
    print("Option Price:", price)
    crr.plot_tree()

    # Plot the tree
    crr.plot_tree()
