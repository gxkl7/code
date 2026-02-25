from abc import ABC, abstractmethod

class CafeOrderHandler(ABC):
    """
    A stateful representation of the interaction between a client and server
    for placing an order.
    """

    @abstractmethod
    def handle_list_menu(self):
        """
        Handle a request for the list of menu items. A typical implementation
        will locate the list of items (e.g. in a database) and call the
        protocol interpreter's `send_list_menu_response` method to send the
        list back to the client.
        :return: None
        """
        pass

    @abstractmethod
    def handle_list_order(self):
        """
        Handle a request for the list of ordered items. A typical implementation
        will call the protocol interpreter's `send_list_order_response` method to send
        the list of ordered menu items back to the client.
        :return: None
        """
        pass

    @abstractmethod
    def handle_add_item(self, item_number: int):
        """
        Handle a request to add an item to the order. A typical implementation
        will validate the requested item number, update state, and then call the
        protocol interpreter's `send_add_item_response` to send the response to the
        client. If the requested item number is invalid, the interpreter's
        `send_error_response` will be called instead.
        :return: None
        """
        pass

    @abstractmethod
    def handle_remove_item(self, item_number: int):
        """
        Handle a request to remove an item from the order. A typical implementation
        will validate the requested item number, update state, and then call the
        protocol interpreter's `send_remove_item_response` to send the response to the
        client. If the requested item number is invalid, the interpreter's
        `send_error_response` will be called instead.
        :return: None
        """
        pass

    @abstractmethod
    def handle_commit_order(self, settlement_token: str):
        """
        Handle a request to commit the order. A typical implementation will invoke
        a service method to commit the state of the order for fulfillment, and then
        call the protocol interpreter's `send_commit_order_response` to send the
        response to the client.
        :param settlement_token: some token that proves the customer paid for the order
        :return: None
        """
        pass

    @abstractmethod
    def handle_cancel_order(self):
        """
        Handle a request to cancel the order. A typical implementation will invoke
        a service method to cancel the order for fulfillment, and then call the protocol
        interpreter's `send_cancel_order_response` to send the response to the client.
        :return:
        """
        pass


