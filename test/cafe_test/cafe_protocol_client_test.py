
from pytest import fixture, raises

from cafe import CafeIO, CafeProtocolClient, CafeClientError, CafeServerError


class MockCafeIO(CafeIO):
    """
    A mock implementation of the `CafeIO` contract.
    """
    def __init__(self):
        # We can append strings to the `response_strings` list to specify
        # the sequence of strings that will be returned when our client calls
        # the `read_string` method.
        self.response_strings = []
        # When the client calls `write_string` to send a request message,
        # the string argument it passes in the call is stored in the `request_string`
        # attribute. We can inspect in our test case to determine what the client
        # requested.
        self.request_string = None
        # This attribute is used in returning the sequence of response strings for each
        # call to read_string.
        self.response_index = 0

    def read_string(self) -> str:
        s = self.response_strings[self.response_index]
        self.response_index += 1
        return s

    def write_string(self, s: str):
        self.request_string = s


@fixture
def mock_io():
    return MockCafeIO()


@fixture
def client_protocol(mock_io: MockCafeIO):
    return CafeProtocolClient(mock_io)


def test_list_menu_items(client_protocol: CafeProtocolClient, mock_io: MockCafeIO):
    # If call client_protocol.send_list_menu_request, it should send the LIST MENU
    # request message. The response from the server will be a list of menu item names.
    # See the Lecture 1 slides for an example. We want to validate that the client
    # sends the expected request message, and that it properly parses the response
    # from the server.

    # Here we set up the sequence of strings that make up the response the client
    # will get when it makes a request. We're pretending that the cafe is out of
    # many items that would normally be on the menu, so the menu item numbers
    # aren't sequential.
    mock_io.response_strings.append("OK 3")
    mock_io.response_strings.append("0 Cheeseburger")
    mock_io.response_strings.append("4 Chips")
    mock_io.response_strings.append("9 Iced Tea")

    # Now we tell the client to "send" a LIST MENU request.
    items = client_protocol.send_menu_items_request()

    # Here we validate that the call to `send_menu_items_request` resulted in a LIST MENU
    # message being "sent" to the server (via our MockCafeIO object).
    assert mock_io.request_string == "LIST MENU"

    # Now we validate that the client correctly parses the server's response into a list
    # of tuples. Each tuple should contain the menu item ID, and the correspondng menu item name.
    assert len(items) == 3
    assert items[0] == (0, "Cheeseburger")
    assert items[1] == (4, "Chips")
    assert items[2] == (9, "Iced Tea")


def test_add_item_ok(client_protocol: CafeProtocolClient, mock_io: MockCafeIO):
    # When we call client_protocol.send_add_item_request, the client should send an
    # ADD request message with the non-negative integer that corresponds to the item
    # number we told it to add. The response from the server is OK followed by an
    # informational message.

    # Here we set up the response the client will get when it makes a request.
    mock_io.response_strings.append("OK item added")

    # Now we call the `send_add_item_request` method for some item number.
    client_protocol.send_add_item_request(42)
    # We just need to confirm that the client sent the correct request message.
    assert mock_io.request_string == "ADD 42"


def test_add_item_error(client_protocol: CafeProtocolClient, mock_io: MockCafeIO):
    # If the client sends a request to add a menu item that is deemed invalid,
    # the server will respond with an ERROR message. Our client implementation
    # interprets the ERROR response and raises an exception that our UI code can
    # catch to decide how best to handle the error. What we want to test here is
    # that when the server response is ERROR the expected exception is raised
    # and that it has the informational message from the server's response.

    # First we set up for an ERROR response message.
    mock_io.response_strings.append("ERROR bad item number")

    # We use Python's `with` construct and the `raises` function imported from Pytest.
    # This allows us to validate that the method we're calling raises the exception
    # that we're expecting. The `raises` function takes the name of an exception type
    # as an argument. The `as` clause allows us to assign the exception (if it is raised)
    # to a variable so we can inspect the exception object. If the exception we expect
    # isn't raised, the `raises` function will cause the test to fail.
    with raises(CafeClientError) as err:
        client_protocol.send_add_item_request(-42)

    # Here we're just checking the error message in the exception object
    # contains the informational message from the server's response. We use
    # Python's `str` function to get a string representation of the exception,
    # which will include any error message that was passed to the exception
    # constructor,
    assert "bad item" in str(err)


#
# Write similar test cases for the other (public) methods on the CafeProtocolClient class
#
