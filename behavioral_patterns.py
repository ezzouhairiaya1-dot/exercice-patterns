"""Behavioral patterns: they organise communication and responsibilities.

1. Strategy        : interchangeable algorithms in separate classes
2. Template Method : a fixed algorithm skeleton, subclasses fill in the steps
"""

from abc import ABC, abstractmethod


# ====================================================================
# 1. STRATEGY
# Problem: a cart applies different discounts. A long if/elif chain
#          on the discount type is hard to extend.
# Idea: each discount is its own class with the same method apply();
#       the cart receives the one to use and can switch at runtime.
# ====================================================================
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price):
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, price):
        return price


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent):
        self._percent = percent

    def apply(self, price):
        return price * (1 - self._percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount):
        self._amount = amount

    def apply(self, price):
        return max(price - self._amount, 0)    # never below zero


class Cart:
    def __init__(self, strategy=None):
        self._items = []
        self._strategy = strategy or NoDiscount()

    def add_item(self, name, price):
        self._items.append((name, price))

    def set_strategy(self, strategy):          # change the algorithm at runtime
        self._strategy = strategy

    def total(self):
        subtotal = sum(price for _, price in self._items)
        return round(self._strategy.apply(subtotal), 2)


# ====================================================================
# 2. TEMPLATE METHOD
# Problem: several data pipelines follow the same steps (load, clean,
#          transform, export), only some steps differ.
# Idea: the superclass run() fixes the order of the steps; subclasses
#       override only the steps that change.
# ====================================================================
class DataPipeline(ABC):
    def run(self):
        """The template method: the skeleton. Subclasses do not override it."""
        data = self.load()
        data = self.clean(data)
        result = self.transform(data)
        self.export(result)
        return result

    @abstractmethod
    def load(self):                            # step every subclass must write
        pass

    def clean(self, data):                     # hook with a default behaviour
        return [item.strip() for item in data]

    @abstractmethod
    def transform(self, data):                 # step every subclass must write
        pass

    def export(self, result):                  # default behaviour
        print("Result:", result)


class SalesPipeline(DataPipeline):
    def load(self):
        return ["  100 ", "250", "  50"]

    def transform(self, data):
        return sum(int(x) for x in data)       # total sales


class NamesPipeline(DataPipeline):
    def load(self):
        return ["  aya ", "tom", " lea  "]

    def transform(self, data):
        return [name.capitalize() for name in data]

    def export(self, result):                  # overrides the default step
        print("Names:", ", ".join(result))


# ====================================================================
# Demo
# ====================================================================
if __name__ == "__main__":
    print("--- Strategy")
    cart = Cart()
    cart.add_item("Book", 20)
    cart.add_item("Pen", 5)
    print("No discount:", cart.total())

    cart.set_strategy(PercentageDiscount(10))
    print("10% off:", cart.total())

    cart.set_strategy(FixedDiscount(8))
    print("8 EUR off:", cart.total())

    print("\n--- Template Method")
    SalesPipeline().run()
    NamesPipeline().run()
