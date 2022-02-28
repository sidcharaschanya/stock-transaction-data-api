from platform import StockTradingPlatform
from trade import Trade
from trade_tree import TradeTree


class TestSets:
    def trade_gen_many_same_stock(self, stock: str = "HSBA", low: int = 1, high: int = 100000) -> list[Trade]:
        pass

    def trade_gen_many_same_value(self, value: float) -> list[Trade]:
        pass

    def trade_gen_many(self, low: int = 1, high: int = 100000) -> list[Trade]:
        pass

    def tree_gen_many_same_val(self, value: float, stock: str = "HSBA") -> TradeTree:
        pass

    def tree_gen_many(self, low: int = 1, high: int = 100000) -> TradeTree:
        pass

    def platform_gen_many_same_stock(self, stock: str, low: int = 1, high: int = 100000) -> StockTradingPlatform:
        pass

    def platform_gen_many_same_val(self, value: float) -> StockTradingPlatform:
        pass

    def platform_gen_many(self, low: int = 1, high: int = 100000) -> StockTradingPlatform:
        pass
