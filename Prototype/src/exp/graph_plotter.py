from src.exp.experimental_framework import Case, ExperimentalFramework
import matplotlib.pyplot as plt
from numpy import unique, polyfit, poly1d, log2


class GraphPlotter:
    def __init__(self, n_transactions: int, n_step: int, n_trials: int) -> None:
        self.__ef = ExperimentalFramework(n_transactions, n_step, n_trials)
        self.__ef.run_tests()
        self.__x = self.__ef.get_n_transactions_list()

    @staticmethod
    def __get_bounds(y) -> tuple[float, float]:
        y.sort()
        return 0.25 * y[int(len(y) * 0.02)], y[int(len(y) * 0.97)] * 1.2

    def __general_plot(self, title, y, y2=None, y1_label=None, y2_label=None, best_func=lambda x: x):
        if y1_label and y2_label:
            plt.plot(self.__x, y, '+', label=y1_label)
            if y2:
                plt.plot(self.__x, y2, '*', label=y2_label)
            plt.legend()
        else:
            plt.plot(self.__x, y, '+')
            if y2:
                plt.plot(self.__x, y2, 'g*')

        plt.plot(self.__x, poly1d(polyfit(best_func(self.__x), y, 1))(best_func(self.__x)), 'b--')
        if y2:
            plt.plot(self.__x, poly1d(polyfit(best_func(self.__x), y2, 1))(best_func(self.__x)), 'g--')
        plt.xlabel("Input Size")
        plt.ylabel("Time of execution")
        plt.title(title)
        plt.ylim(list(self.__get_bounds(y)))
        plt.show()

    def plot_graphs(self):
        self.__general_plot('Log Transactions',
                            self.__ef.get_times(Case.LOG_SORTED),
                            self.__ef.get_times(Case.LOG_RANDOM),
                            'Sorted', 'Random', lambda x: log2(x))
        self.__general_plot('Sorted List Retrieval',
                            self.__ef.get_times(Case.SORTED))
        self.__general_plot('Min Transactions',
                            self.__ef.get_times(Case.MIN), best_func=lambda x: log2(x))
        self.__general_plot('Max Transactions',
                            self.__ef.get_times(Case.MAX), best_func=lambda x: log2(x))
        self.__general_plot('Retrieve Floor',
                            self.__ef.get_times(Case.FLOOR_RANDOM),
                            self.__ef.get_times(Case.FLOOR_EXISTING),
                            'Random', 'Existing', lambda x: log2(x))
        self.__general_plot('Retrieve Ceiling',
                            self.__ef.get_times(Case.CEILING_RANDOM),
                            self.__ef.get_times(Case.CEILING_EXISTING),
                            'Random', 'Existing', lambda x: log2(x))
        self.__general_plot('Retrieve Range',
                            self.__ef.get_times(Case.RANGE_ALL),
                            self.__ef.get_times(Case.RANGE_RANDOM),
                            'Full range', 'Random Range')


if __name__ == '__main__':
    plotter = GraphPlotter(10000, 100, 30)
    plotter.plot_graphs()
