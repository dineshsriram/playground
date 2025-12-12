"""
Given an input string: "UK:US:FedEx:4,UK:FR:Jet1:2,US:UK:RyanAir:8,CA:UK:CanadaAir:8"
Which represents flights between destinations in the format: "Source:Destination:Airline:Cost,..."

Write a function which will take a Source and Destination and output the cost.

(Building from the first question)
Write a function which will take an Input String, Source and Destination that have no direct connecting flight,
and output a route that you can take to reach the destination.
The output should be in the format: return {'route': 'US -> UK -> FR', 'method': 'RyanAir -> Jet1', 'cost': 10}
"""

from collections import deque
from collections import defaultdict
from decimal import Decimal
from typing import NamedTuple, Sequence


class ShippingConnection(NamedTuple):
    source: str
    destination: str
    airline: str
    cost: Decimal

    @classmethod
    def from_str(cls, shipping_data: str) -> ShippingConnection:
        data = shipping_data.split(":")
        return cls(data[0], data[1], data[2], Decimal(data[3]))


class Route(NamedTuple):
    stops: tuple[str]
    airlines: tuple[str]
    cost: Decimal


class ShippingCostCalculator:

    def __init__(self, shipping_connections: Sequence[ShippingConnection]):
        self.shipping_connections = tuple(shipping_connections)
        self.routes_from = self._build_routes_map(self.shipping_connections)

    def _build_routes_map(
        self, shipping_connections: tuple[ShippingConnection]
    ) -> dict[str, list[ShippingConnection]]:
        cost_lookup: dict[str, list[ShippingConnection]] = defaultdict(list)
        for connection in shipping_connections:
            cost_lookup[connection.source].append(connection)
        return cost_lookup

    def calculate_cost(self, source: str, destination: str) -> Route:
        connection_queue = deque([Route((source,), (), Decimal(0))])
        visited: set[str] = {source}

        while connection_queue:
            current_route = connection_queue.popleft()

            for connection in self.routes_from.get(current_route.stops[-1], ()):
                if connection.destination == destination:
                    return Route(
                        current_route.stops + (connection.destination,),
                        current_route.airlines + (connection.airline,),
                        current_route.cost + connection.cost,
                    )

                if connection.destination not in visited:
                    connection_queue.append(
                        Route(
                            current_route.stops + (connection.destination,),
                            current_route.airlines + (connection.airline,),
                            current_route.cost + connection.cost,
                        )
                    )
                    visited.add(connection.destination)

        raise LookupError(f"No route found from '{source}' to '{destination}'")

    @classmethod
    def from_str(cls, input_data: str) -> ShippingCostCalculator:
        return ShippingCostCalculator(
            (
                ShippingConnection.from_str(shipping_data)
                for shipping_data in input_data.split(",")
            )
        )


if __name__ == "__main__":
    calc = ShippingCostCalculator.from_str(
        "UK:US:FedEx:4,UK:FR:Jet1:2,US:UK:RyanAir:8,CA:UK:CanadaAir:8"
    )

    for source, destination in {"US": "FR", "UK": "US", "CA": "US"}.items():
        tracker = calc.calculate_cost(source, destination)
        print(f"{source} -> {destination}: {tracker}")
