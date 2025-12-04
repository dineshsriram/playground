from decimal import Decimal
from strategy_pattern import Customer, Item, Order, fidelity_discount
import pytest


@pytest.fixture
def test_customer() -> Customer:
    return Customer("Dinesh", Decimal("2000.00"))


@pytest.fixture
def single_item() -> Item:
    return Item("Shirt", 1, Decimal("59.99"))


@pytest.fixture
def multiple_quantity_item() -> Item:
    return Item("Cap", 10, Decimal("999.99"))


@pytest.fixture
def one_item_order(test_customer: Customer, single_item: Item) -> Order:
    return Order(customer=test_customer, cart=[single_item])


@pytest.fixture
def multiple_item_order(
    test_customer: Customer, single_item: Order, multiple_quantity_item: Item
) -> Order:
    return Order(customer=test_customer, cart=[single_item, multiple_quantity_item])


class TestItem:
    def test_item_total(self):
        item = Item("Bra", 2, Decimal("599.99"))
        assert item.total() == Decimal("1199.98")


class TestOrder:
    def test_create_order(self):
        customer = Customer("Dinesh", Decimal("100.00"))
        cart = [Item("Shirt", 1, Decimal(59.99))]
        order = Order(customer=customer, cart=cart)
        assert ("Dinesh", Decimal("100.00")) == (
            order.customer.name,
            order.customer.points,
        )
        assert 1 == len(order.cart)

    def test_single_item_order_total(self, one_item_order: Order):
        assert one_item_order.total() == Decimal("59.99")

    def test_multiple_item_order_total(self, multiple_item_order: Order):
        assert multiple_item_order.total() == Decimal("10059.89")

    def test_order_with_fidelity_discount(self, one_item_order: Order):
        total = one_item_order.total()
        total_with_discount = fidelity_discount(one_item_order)
        assert total_with_discount == Decimal(0.05) * total
