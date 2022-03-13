from src.exp.experimental_framework import ExperimentalFramework
import matplotlib.pyplot as plt
import numpy as np
import random


class GraphPlotter:
    def __init__(self, ef: ExperimentalFramework) -> None:
        self.__ef = ef
        random.seed("Algorithms (COMP0005)")
        self.__ef.run_tests()
        self.__x = self.__ef.get_n_transactions_list()

    @staticmethod
    def __get_y_lim(ys: list) -> list:
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
            plt.legend(loc = "upper left")

        plt.title(op + " Time Vs. Transaction Count")
        plt.xlabel("Number of Transactions Under a Particular Stock")
        plt.ylabel("Execution Time (s)")
        plt.ylim(self.__get_y_lim(ys))
        plt.show()

    def plot_graphs(self) -> None:
        self.__general_plot(
            "Log Transaction",
            [
                self.__ef.get_times(ExperimentalFramework.LOG_RANDOM),
                self.__ef.get_times(ExperimentalFramework.LOG_SORTED)
            ],
            ["m", "b"],
            [np.log2, np.log2],
            ["Random Insertion Order", "Sorted Insertion Order"]
        )

        self.__general_plot(
            "Sorted Transactions",
            [self.__ef.get_times(ExperimentalFramework.SORTED)],
            ["b"],
            [lambda x: x]
        )

        self.__general_plot(
            "Min Transactions",
            [self.__ef.get_times(ExperimentalFramework.MIN)],
            ["r"],
            [np.log2]
        )

        self.__general_plot(
            "Max Transactions",
            [self.__ef.get_times(ExperimentalFramework.MAX)],
            ["g"],
            [np.log2]
        )

        self.__general_plot(
            "Floor Transactions",
            [
                self.__ef.get_times(ExperimentalFramework.FLOOR_RANDOM),
                self.__ef.get_times(ExperimentalFramework.FLOOR_EXISTING)
            ],
            ["r", "b"],
            [np.log2, np.log2],
            ["Random Threshold Values", "Threshold Values Existing in Tree"]
        )

        self.__general_plot(
            "Ceiling Transactions",
            [
                self.__ef.get_times(ExperimentalFramework.CEILING_RANDOM),
                self.__ef.get_times(ExperimentalFramework.CEILING_EXISTING)
            ],
            ["g", "b"],
            [np.log2, np.log2],
            ["Random Threshold Values", "Threshold Values Existing in Tree"]
        )

        self.__general_plot(
            "Range Transactions",
            [
                self.__ef.get_times(ExperimentalFramework.RANGE_RANDOM),
                self.__ef.get_times(ExperimentalFramework.RANGE_ALL)
            ],
            ["c", "b"],
            [lambda x: x, lambda x: x],
            ["Random Range", "Full Range"]
        )


if __name__ == '__main__':
    plotter = GraphPlotter(ExperimentalFramework(10000, 100, 20))
    plotter.plot_graphs()
