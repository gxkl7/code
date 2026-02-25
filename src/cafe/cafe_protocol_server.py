
from .cafe_order_handler import CafeOrderHandler
from .cafe_io import CafeIO

class CafeProtocolServer:
    """
    An interpreter for the server side of the Sad Cafe protocol. The interpreter is
    responsible for intake of client requests and dispatching to appropriate methods
    of an injected `CafeClientHandler`. It also provides methods that can be used to
    send appropriately formatted responses to the client.
    """

    def __init__(self, handler: CafeOrderHandler, io: CafeIO):
        """
        Initializes this instance of the protocol interpreter.
        :param handler: the handler to which requested actions will be delegated
        :param io: the I/O channel to use in receiving and sending protocol
            messages to the client
        """
        self._handler = handler
        self._io = io

    def _send_unrecognized_request_error(self, words: list[str]):
        self.send_error_response(f"unrecognized {words[0]} request")

    def _parse_item_number(self, s: str) -> int:
        try:
            item_number = int(s)
            if item_number < 0:
                raise ValueError
            return item_number
        except ValueError:
            self.send_error_response("invalid item number")
            return -1
    
    def _parse_list_request(self, words: list[str]):
        if len(words) != 2:
            self._send_unrecognized_request_error(words)
        elif words[1] == "MENU":
            self._handler.handle_list_menu()
        elif words[1] == "ORDER":
            self._handler.handle_list_order()
        else:
            self._send_unrecognized_request_error(words)

    def _parse_add_request(self, words: list[str]):
        if len(words) != 2:
            self._send_unrecognized_request_error(words)
        else:
            item_number = self._parse_item_number(words[1])
            if item_number >= 0:
                self._handler.handle_add_item(item_number)

    def _parse_remove_request(self, words: list[str]):
        if len(words) != 2:
            self._send_unrecognized_request_error(words)
        else:
            item_number = self._parse_item_number(words[1])
            if item_number >= 0:
                self._handler.handle_remove_item(item_number)

    def _parse_commit_request(self, words: list[str]):
        if len(words) != 2:
            self._send_unrecognized_request_error(words)
        else:
            settlement_token = words[1]
            self._handler.handle_commit_order(settlement_token)

    def _parse_cancel_request(self, words: list[str]):
        if len(words) != 1:
            self._send_unrecognized_request_error(words)
        else:
            self._handler.handle_cancel_order()

    def receive_next_request(self):
        """
        Waits for the next request to be received from the client,
        and dispatches the request accordingly.
        :return: None
        """
        request = self._io.read_string()
        assert request is not None and request.strip() != ""
        words = [word.upper() for word in request.split()]
        if words[0] == "LIST":
            self._parse_list_request(words)
        elif words[0] == "ADD":
            self._parse_add_request(words)
        elif words[0] == "REMOVE":
            self._parse_remove_request(words)
        elif words[0] == "COMMIT":
            self._parse_commit_request(words)
        elif words[0] == "CANCEL":
            self._parse_cancel_request(words)
        else:
            self.send_error_response("unrecognized request action")

    def send_menu_items_response(self, items: list[str]):
        """
        Sends a response containing the list of menu items.
        :param items: list of strings representing menu items
        :return: None
        """
        self._io.write_string(f"OK {len(items)}")
        for i, item in enumerate(items):
            self._io.write_string(f"{i} {item}")

    def send_order_items_response(self, items: list[int]):
        """
        Sends a response containing the list of items on the order
        :param items: list of each containing a menu item number
        :return: None
        """
        self._io.write_string(f"OK {len(items)}")
        for i, item_id in enumerate(items):
            self._io.write_string(f"{i} {item_id}")

    def send_add_item_response(self, num_items: int):
        """
        Sends the response for a request to add an item to the order.
        :param num_items: the number of items now on the order
        :return: None
        """
        self._io.write_string(f"OK order has {num_items} item(s)")

    def send_remove_item_response(self, item_number: int):
        """
        Sends the response for a request to remove an item from the order.
        :param item_number: the item number that was requested to be removed
        :return: None
        """
        self._io.write_string(f"OK removed item {item_number}")

    def send_commit_order_response(self, order_number: int):
        """
        Sends the response for a request to commit the order.
        :param order_number: a reference number for the committed order
        :return: None
        """
        self._io.write_string(f"OK {order_number}")

    def send_cancel_order_response(self):
        """
        Sends the response for a request to cancel the order.
        :return: None
        """
        self._io.write_string(f"OK canceled")

    def send_error_response(self, message: str):
        """
        Sends en response to the client, containing the given error message.
        :param message: the message to be sent
        :return: None
        """
        self._io.write_string(f"ERROR {message}")

