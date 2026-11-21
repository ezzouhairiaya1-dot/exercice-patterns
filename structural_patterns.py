"""Structural patterns: they assemble objects into larger structures.

1. Adapter   : make two incompatible interfaces work together
2. Decorator : add behaviour to an object by wrapping it
"""

from abc import ABC, abstractmethod


# ====================================================================
# 1. ADAPTER
# Problem: the shop expects pay(amount_eur), but an old bank class we
#          cannot modify offers make_transaction(amount_cents).
# Idea: an adapter implements the interface the shop expects and
#       translates the call to the old class.
# ====================================================================
class PaymentProcessor(ABC):          # the interface the shop expects
    @abstractmethod
    def pay(self, amount_eur):
        pass


class CardProcessor(PaymentProcessor):    # already compatible
    def pay(self, amount_eur):
        return f"Card payment of {amount_eur:.2f} EUR done"


class LegacyBank:                     # old class, different interface
    def make_transaction(self, amount_cents):
        return f"Legacy bank: transaction of {amount_cents} cents done"


class LegacyBankAdapter(PaymentProcessor):
    def __init__(self, legacy_bank):
        self._bank = legacy_bank

    def pay(self, amount_eur):
        cents = int(round(amount_eur * 100))     # euros -> cents
        return self._bank.make_transaction(cents)


class Shop:
    def checkout(self, processor, amount_eur):
        # The shop only knows PaymentProcessor, not the legacy class.
        return processor.pay(amount_eur)


# ====================================================================
# 2. DECORATOR
# Problem: an order can get options (gift wrap, express shipping,
#          insurance) in any combination. Subclasses for each
#          combination would explode.
# Idea: each option is a wrapper with the same interface as the order.
# ====================================================================
class Order(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass


class BasicOrder(Order):
    def __init__(self, item, price):
        self._item = item
        self._price = price

    def cost(self):
        return self._price

    def description(self):
        return self._item


class OrderDecorator(Order):          # base wrapper: holds the wrapped order
    def __init__(self, order):
        self._order = order           # protected, so subclasses can use it

    def cost(self):
        return self._order.cost()

    def description(self):
        return self._order.description()


class GiftWrap(OrderDecorator):
    def cost(self):
        return self._order.cost() + 3

    def description(self):
        return self._order.description() + " + gift wrap"


class ExpressShipping(OrderDecorator):
    def cost(self):
        return self._order.cost() + 10

    def description(self):
        return self._order.description() + " + express shipping"


class Insurance(OrderDecorator):
    def cost(self):
        return self._order.cost() + 5

    def description(self):
        return self._order.description() + " + insurance"


# ====================================================================
# Demo
# ====================================================================
if __name__ == "__main__":
    print("--- Adapter")
    shop = Shop()
    print(shop.checkout(CardProcessor(), 19.99))
    print(shop.checkout(LegacyBankAdapter(LegacyBank()), 19.99))

    print("\n--- Decorator")
    order = BasicOrder("Book", 20)
    print(order.description(), "=", order.cost(), "EUR")

    order = GiftWrap(order)
    order = ExpressShipping(order)    # wrappers can be stacked
    print(order.description(), "=", order.cost(), "EUR")

    other = Insurance(GiftWrap(BasicOrder("Headphones", 80)))
    print(other.description(), "=", other.cost(), "EUR")
