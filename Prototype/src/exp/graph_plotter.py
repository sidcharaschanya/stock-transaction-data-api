from src.exp.experimental_framework import ExperimentalFramework
import matplotlib.pyplot as plt


class GraphPlotter:
    def __init__(self, n_transactions: int, n_step: int, n_trials: int) -> None:
        self.n_transactions = n_transactions
        self.n_step = n_step
        self.n_trials = n_trials
        self.ef = ExperimentalFramework(self.n_transactions, self.n_step, self.n_trials)


plotter = GraphPlotter(10000, 50, 5)
