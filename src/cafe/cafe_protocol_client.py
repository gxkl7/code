from .cafe_io import CafeIO

class CafeServerError(Exception):
    """
    A custom exception type raised when the server sends an invalid response.
    """
    pass


class CafeClientError(Exception):
    """
    A custom exception type raised if the server indicates that we sent an invalid
    request.
    """
    pass


class CafeProtocolClient:
    """
    An interpreter for the client side of the Sad Cafe protocol. The interpreter is
    responsible for sending properly formatted protocol requests, and decoding
    responses for return to the caller.
    """

    def __init__(self, io: CafeIO):
        """
        Initializes this instance of the protocol interpreter.
        :param io: the I/O channel to use in receiving and sending protocol
            messages to the client
        """
        self._io = io

    def _await_response(self) -> str:
        """
        Reads the first message of a server response.
        :return: the string following OK in the server's response
        :raises CafeClientError: if the server's response is ERROR
        :raises CafeServerError: if the server's response is unrecognized
        """
        response = self._io.read_string()
        assert response is not None and response.strip() != ""
        status, message = response.split(maxsplit=1)
        status = status.upper()
        if status == "OK":
            return message
        elif status == "ERROR":
            raise CafeClientError(message)
        else:
            raise CafeServerError(f"invalid server response '{response}")

    def _await_number_response(self) -> int:
        """
        Reads the first message of a server response that should contain a number after OK.
        :return: the number following OK in the server's response
        :raises CafeClientError: if the server's response is ERROR
        :raises CafeServerError: if the server's response is unrecognized
        """
        s = self._await_response()
        try:
            return int(s)
        except ValueError:
            raise CafeServerError(f"invalid number in OK response {s}")

    def _await_list_response(self) -> list[tuple[int, str]]:
        """
        Reads a server list response. The first line of the response is
        OK followed by the number of items, N. The next N lines are tuples
        of the form `k label`, where k is a non-negative integer, and `label`
        is a string.
        :return: the list of tuples found in the response
        :raises CafeClientError: if the server's response is ERROR
        :raises CafeServerError: if the server's response is unrecognized
        """
        items: list[tuple[int, str]] = []
        num_items = self._await_number_response()
        for _ in range(num_items):
            item = self._io.read_string()
            assert item is not None and item.strip() != ""
            k, label = item.split(maxsplit=1)
            try:
                items.append((int(k), label))
            except ValueError:
                raise CafeServerError(f"invalid item number in list items {k}")
        return items

    def send_menu_items_request(self) -> list[tuple[int, str]]:
        """
        Sends a request for the available menu items.
        :return: list of tuples, each containing an item number and string label
        :raises CafeClientError: if the server response is ERROR
        :raises CafeServerError: if the server response is invalid
        """
        self._io.write_string("LIST MENU")
        return self._await_list_response()

    def send_order_items_request(self) -> list[tuple[int, str]]:
        """
        Sends a request for the items in the client's order.
        :return: list of tuples, each containing an item index and string label
        :raises CafeClientError: if the server response is ERROR
        :raises CafeServerError: if the server response is invalid
        """
        self._io.write_string("LIST ORDER")
        return self._await_list_response()

    def send_add_item_request(self, item_number: int):
        """
        Sends a request to add an item to the order.
        :param item_number: the menu item number to add
        :return: None
        :raises CafeClientError: if the server response is ERROR
        :raises CafeServerError: if the server response is invalid
        """
        self._io.write_string(f"ADD {item_number}")
        return self._await_response()

    def send_remove_item_request(self, item_number: int):
        """
        Sends a request to remove an item from the order.
        :param item_number: the index of the item number to remove
        :return: None
        :raises CafeClientError: if the server response is ERROR
        :raises CafeServerError: if the server response is invalid
        """
        self._io.write_string(f"REMOVE {item_number}")
        return self._await_response()

    def send_commit_order_response(self, settlement_token: str) -> int:
        """
        Sends a request to commit the order.
        :param settlement_token: some token that proves the customer paid for the order
        :return: reference number for the order
        :raises CafeClientError: if the server response is ERROR
        :raises CafeServerError: if the server response is invalid
        """
        self._io.write_string(f"COMMIT {settlement_token}")
        return self._await_number_response()

    def send_cancel_order_response(self):
        """
        Sends a request to cancel the order.
        :return: None
        :raises CafeClientError: if the server response is ERROR
        :raises CafeServerError: if the server response is invalid
        """
        self._io.write_string(f"CANCEL")
        return self._await_response()

