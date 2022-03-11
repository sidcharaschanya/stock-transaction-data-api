from src.exp.experimental_framework import Case, ExperimentalFramework
import matplotlib.pyplot as plt
import numpy as np
import typing as t


class GraphPlotter:
    def __init__(self, n_transactions: int, n_step: int, n_trials: int) -> None:
        self.__ef = ExperimentalFramework(n_transactions, n_step, n_trials)
        self.__ef.run_tests()
        self.__x = self.__ef.get_n_transactions_list()

    @staticmethod
    def __get_bounds(y: list) -> t.List[float]:
        y.sort()
        return [0.2 * y[int(len(y) * 0.03)], y[int(len(y) * 0.97)] * 1.2]

    def __general_plot(self, title: str, ys: list, colors: list, funcs: list, labels: list = None) -> None:
        for i, (y, color, func) in enumerate(zip(ys, colors, funcs)):
            if labels:
                plt.plot(self.__x, y, color + ".", label = labels[i])
            else:
                plt.plot(self.__x, y, color + ".")

            plt.plot(self.__x, np.poly1d(np.polyfit(func(self.__x), y, 1))(func(self.__x)), color + "--")

        plt.title(title)
        plt.xlabel("Number of Transactions Under a Particular Stock")
        plt.ylabel("Time of Execution (s)")
        plt.ylim(self.__get_bounds(ys[0]))

        if labels:
            plt.legend()

        plt.show()

    def plot_graphs(self):
        self.__general_plot(
            "Log Transactions",
            [self.__ef.get_times(Case.LOG_RANDOM), self.__ef.get_times(Case.LOG_SORTED)],
            ["b", "m"],
            [np.log2, np.log2],
            ["Random", "Sorted"]
        )

        self.__general_plot(
            "Sorted List Retrieval",
            [self.__ef.get_times(Case.SORTED)],
            ["c"],
            [lambda x: x]
        )

        self.__general_plot(
            "Min Transactions",
            [self.__ef.get_times(Case.MIN)],
            ["g"],
            [np.log2]
        )

        # self.__general_plot('Max Transactions',
        #                     self.__ef.get_times(Case.MAX), best_func = lambda x: log2(x))
        # self.__general_plot('Retrieve Floor',
        #                     self.__ef.get_times(Case.FLOOR_RANDOM),
        #                     self.__ef.get_times(Case.FLOOR_EXISTING),
        #                     'Random', 'Existing', lambda x: log2(x))
        # self.__general_plot('Retrieve Ceiling',
        #                     self.__ef.get_times(Case.CEILING_RANDOM),
        #                     self.__ef.get_times(Case.CEILING_EXISTING),
        #                     'Random', 'Existing', lambda x: log2(x))
        # self.__general_plot('Retrieve Range',
        #                     self.__ef.get_times(Case.RANGE_ALL),
        #                     self.__ef.get_times(Case.RANGE_RANDOM),
        #                     'Full range', 'Random Range')


if __name__ == '__main__':
    plotter = GraphPlotter(10000, 100, 5)
    plotter.plot_graphs()
