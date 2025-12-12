from decimal import Decimal
import pytest
from .shipping_cost import ShippingConnection, ShippingCostCalculator


class TestShippingConnection:

    test_data = [
        (
            "UK:US:FedEx:4",
            ShippingConnection(
                source="UK", destination="US", airline="FedEx", cost=Decimal(4)
            ),
        ),
        (
            "UK:FR:Jet1:2",
            ShippingConnection(
                source="UK", destination="FR", airline="Jet1", cost=Decimal(2)
            ),
        ),
    ]

    @pytest.mark.parametrize("input_str, expected", test_data)
    def test_parse_shipping_connection_strings(self, input_str, expected):
        assert ShippingConnection.from_str(input_str) == expected


class TestShippingCostCalculator:

    def test_parse_str(self):
        input = "UK:US:FedEx:4,UK:FR:Jet1:2"
        calculator = ShippingCostCalculator.from_str(input)

        assert calculator.shipping_connections == (
            ShippingConnection(
                source="UK", destination="US", airline="FedEx", cost=Decimal(4)
            ),
            ShippingConnection(
                source="UK", destination="FR", airline="Jet1", cost=Decimal(2)
            ),
        )
