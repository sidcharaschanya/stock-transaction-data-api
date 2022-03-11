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
    def __get_y_lim(ys: t.List[list]) -> t.List[float]:
        return [
            min([sorted(y)[0] * 0.75 for y in ys]),
            max([sorted(y)[int((len(y) - 1) * 0.97)] * 1.1 for y in ys])
        ]

    def __general_plot(self, op: str, ys: list, colors: list, funcs: list, labels: list = None) -> None:
        for i, (y, color, func) in enumerate(zip(ys, colors, funcs)):
            if labels:
                plt.plot(self.__x, y, color + ".", label = labels[i])
            else:
                plt.plot(self.__x, y, color + ".")

            plt.plot(self.__x, np.poly1d(np.polyfit(func(self.__x), y, 1))(func(self.__x)), color + "--")

        if labels:
            plt.legend()

        plt.title(op + " Time Vs. Transaction Count")
        plt.xlabel("Number of Transactions Under a Particular Stock")
        plt.ylabel("Execution Time (s)")
        plt.ylim(self.__get_y_lim(ys))
        plt.show()

    def plot_graphs(self) -> None:
        self.__general_plot(
            "Log Transaction",
            [self.__ef.get_times(Case.LOG_RANDOM), self.__ef.get_times(Case.LOG_SORTED)],
            ["m", "b"],
            [np.log2, np.log2],
            ["Random Insertion Order", "Sorted Insertion Order"]
        )

        self.__general_plot(
            "Sorted Transactions",
            [self.__ef.get_times(Case.SORTED)],
            ["b"],
            [lambda x: x]
        )

        self.__general_plot(
            "Min Transactions",
            [self.__ef.get_times(Case.MIN)],
            ["r"],
            [np.log2]
        )

        self.__general_plot(
            "Max Transactions",
            [self.__ef.get_times(Case.MAX)],
            ["g"],
            [np.log2]
        )

        self.__general_plot(
            "Floor Transactions",
            [self.__ef.get_times(Case.FLOOR_RANDOM), self.__ef.get_times(Case.FLOOR_EXISTING)],
            ["r", "b"],
            [np.log2, np.log2],
            ["Random Threshold Values", "Threshold Values Existing in Tree"]
        )

        self.__general_plot(
            "Ceiling Transactions",
            [self.__ef.get_times(Case.CEILING_RANDOM), self.__ef.get_times(Case.CEILING_EXISTING)],
            ["g", "b"],
            [np.log2, np.log2],
            ["Random Threshold Values", "Threshold Values Existing in Tree"]
        )

        self.__general_plot(
            "Range Transactions",
            [self.__ef.get_times(Case.RANGE_RANDOM), self.__ef.get_times(Case.RANGE_ALL)],
            ["c", "b"],
            [lambda x: x, lambda x: x],
            ["Random Range", "Full Range"]
        )


plotter = GraphPlotter(10000, 100, 20)
plotter.plot_graphs()
