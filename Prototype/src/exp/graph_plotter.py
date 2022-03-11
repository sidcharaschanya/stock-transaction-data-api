from src.exp.experimental_framework import Case, ExperimentalFramework
import matplotlib.pyplot as plt


class GraphPlotter:
    def __init__(self, n_transactions: int, n_step: int, n_trials: int) -> None:
        self.__ef = ExperimentalFramework(n_transactions, n_step, n_trials)
        self.__ef.run_tests()
        self.__x = self.__ef.get_n_transactions_list()

    def __plot_log_graph(self) -> None:
        plt.plot(self.__x, self.__ef.get_times(Case.LOG_RANDOM), "+")
        plt.plot(self.__x, self.__ef.get_times(Case.LOG_SORTED), "g*")
        plt.ylim([0.000004, 0.00002])
        plt.show()

    def __plot_sorted_graph(self) -> None:
        plt.plot(self.__x, self.__ef.get_times(Case.SORTED), "+")
        plt.show()

    def __plot_min_graph(self) -> None:
        plt.plot(self.__x, self.__ef.get_times(Case.MIN), "+")
        plt.ylim([0.0000005, 0.00000125])
        plt.show()

    def __plot_max_graph(self) -> None:
        plt.plot(self.__x, self.__ef.get_times(Case.MAX), "+")
        plt.ylim([0.0000005, 0.00000125])
        plt.show()

    def __plot_floor_graph(self) -> None:
        plt.plot(self.__x, self.__ef.get_times(Case.FLOOR_RANDOM), "+")
        plt.plot(self.__x, self.__ef.get_times(Case.FLOOR_EXISTING), "g*")
        plt.ylim([0.0000007, 0.0000021])
        plt.show()

    def __plot_ceiling_graph(self) -> None:
        plt.plot(self.__x, self.__ef.get_times(Case.CEILING_RANDOM), "+")
        plt.plot(self.__x, self.__ef.get_times(Case.CEILING_EXISTING), "g*")
        plt.ylim([0.0000007, 0.0000021])
        plt.show()

    def __plot_range_graph(self) -> None:
        plt.plot(self.__x, self.__ef.get_times(Case.RANGE_RANDOM), "+")
        plt.plot(self.__x, self.__ef.get_times(Case.RANGE_ALL), "g*")
        plt.show()

    def plot_graphs(self):
        self.__plot_log_graph()
        self.__plot_sorted_graph()
        self.__plot_min_graph()
        self.__plot_max_graph()
        self.__plot_floor_graph()
        self.__plot_ceiling_graph()
        self.__plot_range_graph()


plotter = GraphPlotter(10000, 100, 5)
plotter.plot_graphs()
