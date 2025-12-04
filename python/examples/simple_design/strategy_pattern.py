from decimal import Decimal
from typing import Callable, NamedTuple, Sequence


class Customer(NamedTuple):
    name: str
    points: Decimal


class Item(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


class Order(NamedTuple):
    customer: Customer
    cart: Sequence[Item]
    promotion: Callable[[Order], Decimal] | None = None

    def total(self) -> Decimal:
        return sum([item.total() for item in self.cart], start=Decimal("0.0"))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount


# Type variable
Discount = Callable[[Order], Decimal]

# Global variable
g_discounts: list[Discount] = []


# Function registration decorator that takes in a discount function, adds it to a global list and returns the function as is.
def discount(disc: Discount) -> Discount:
    g_discounts.append(disc)
    return disc


@discount
def fidelity_discount(order: Order) -> Decimal:
    if order.customer.points > 1000:
        return Decimal(0.05) * order.total()
    return Decimal(0)


@discount
def bulk_item_discount(order: Order) -> Decimal:
    total_item_discount: Decimal = 0
    for item in order.cart:
        if item.quantity >= 20:
            total_item_discount += Decimal(0.1) * item.total()
    return total_item_discount


@discount
def distinct_item_discount(order: Order) -> Decimal:
    distinct_items_in_cart: set[str] = set([item.product for item in order.cart])
    if len(distinct_items_in_cart) >= 10:
        return Decimal(0.07) * order.total()
    return Decimal(0)


def best_discount():
    """Returns the maximum discount that can be applied to an order"""
    return max([discount() for discount in g_discounts])
