import random

class CafeService:
    """
    A simple service façade representing the order fulfillment service.
    """

    def __init__(self, menu_items: list[str]):
        """
        Initializes this service instance.
        :param menu_items: menu items to be made available for order
        """
        self._next_order_number = random.randrange(100, 1000)
        self._menu_items = menu_items

    def menu_items(self) -> list[str]:
        """
        Gets the list of menu items available for orders.
        :return: list of menu item strings
        """
        return self._menu_items

    def place_order(self, settlement_token: str, ordered_items: list[int]):
        """
        Places an order for fulfillment.
        :param settlement_token: some token that proves the customer paid for the order
        :param ordered_items: the list of menu items for the order
        :return: reference number for the order
        """
        order_number = self._next_order_number
        items = ", ".join([self._menu_items[i] for i in ordered_items])
        print(f"sending order {order_number} to fulfillment; settlement_token={settlement_token} items={items}")
        self._next_order_number += 1
        return order_number
