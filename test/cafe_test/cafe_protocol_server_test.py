from unittest.mock import Mock

from pytest import fixture

from cafe import CafeIO, CafeProtocolServer


class MockCafeIO(CafeIO):
    """
    A mock implementation of the `CafeIO` contract.
    """
    def __init__(self):
        # We can set the `request_string` attribute to control what request
        # message will be "received" when `CafeProtocolServer` calls the `read_string`
        # method.
        self.request_string = None
        # For each call to the `write_string` method, the string passed as an argument
        # is appended to the `response_strings` list. We can inspect the list to see
        # what our protocol server "says" when told to send a response.
        self.response_strings = []

    def read_string(self) -> str:
        return self.request_string

    def write_string(self, s: str):
        self.response_strings.append(s)


# This `fixture` is used by Pytest to provide the objects we need in our
# test cases. In the function definitions that follow, everywhere we
# specify an argument named `mock_io`, Pytest will pass the object that
# is returned by this function.
@fixture
def mock_io():
    return MockCafeIO()


# This `fixture` is used by Pytest to provide the objects we need in our
# test cases. In the function definitions that follow, everywhere we
# specify an argument named `mock_handler`, Pytest will pass the object that
# is returned by this function.
@fixture
def mock_handler():
    return Mock()       # This mock comes from Python's unit testing framework; see import above

# This `fixture` is used by Pytest to provide the objects we need in our
# test cases. Pytest will pass the object that is returned by this function
# to every test case that specifies an argument named `server_protocol`.
@fixture
def server_protocol(mock_handler: Mock, mock_io: MockCafeIO):
    # Here we construct an instance of the our test subject (`CafeProtocolServer`)
    # and inject mock handler and mock IO objects that it will call on as needed
    return CafeProtocolServer(mock_handler, mock_io)


def test_add_item_request(server_protocol: CafeProtocolServer,
                          mock_handler: Mock,
                          mock_io: MockCafeIO):
    # The protocol allows any non-negative integer to be specified
    # in an ADD request. The interpreter should translate it into
    # call to the handler with an integer argument that matches what
    # was requested.
    mock_io.request_string = "ADD 42"
    server_protocol.receive_next_request()
    mock_handler.handle_add_item.assert_called_once_with(42)


def test_add_item_request_with_negative_item_number(server_protocol: CafeProtocolServer,
                                                    mock_handler: Mock,
                                                    mock_io: MockCafeIO):
    # The protocol doesn't allow a negative item number
    # in an ADD request. The interpreter should produce an ERROR response,
    # It shouldn't call the handler's `handle_add_item` method at all.
    mock_io.request_string = "ADD -1"
    server_protocol.receive_next_request()
    mock_handler.handle_add_item.assert_not_called()
    assert len(mock_io.response_strings) > 0
    assert mock_io.response_strings[0].startswith("ERROR ")


def test_remove_item_request(server_protocol: CafeProtocolServer,
                             mock_handler: Mock,
                             mock_io: MockCafeIO):
    # The protocol allows any non-negative integer to be specified
    # in a REMOVE request. The interpreter should translate it into
    # call to the handler with an integer argument that matches what
    # was requested.
    mock_io.request_string = "REMOVE 42"
    server_protocol.receive_next_request()
    mock_handler.handle_remove_item.assert_called_once_with(42)


def test_remove_item_request_with_negative_item_number(server_protocol: CafeProtocolServer,
                             mock_handler: Mock,
                             mock_io: MockCafeIO):
    # The protocol doesn't allow a negative item number
    # in a REMOVE request. The interpreter should produce an ERROR response,
    # It shouldn't call the handler's `handle_remove_item` method at all.
    mock_io.request_string = "REMOVE -1"
    server_protocol.receive_next_request()
    mock_handler.handle_remove_item.assert_not_called()
    assert len(mock_io.response_strings) > 0
    assert mock_io.response_strings[0].startswith("ERROR ")


def test_cancel_order_request(server_protocol: CafeProtocolServer,
                              mock_handler: Mock,
                              mock_io: MockCafeIO):
    # A request to cancel the order should simply invoke the handler's
    # `handle_cancel_order` method.
    mock_io.request_string = "CANCEL"
    server_protocol.receive_next_request()
    mock_handler.handle_cancel_order.assert_called_once()


def test_cancel_order_request_with_extra_args(server_protocol: CafeProtocolServer,
                                              mock_handler: Mock,
                                              mock_io: MockCafeIO):
    # A request to cancel shouldn't have any additional arguments. If it does
    # the interpreter should respond with an error without calling the handler's
    # `handle_cancel_order` method.
    mock_io.request_string = "CANCEL foobar"
    server_protocol.receive_next_request()
    mock_handler.handle_cancel_order.assert_not_called()
    assert len(mock_io.response_strings) > 0
    assert mock_io.response_strings[0].startswith("ERROR ")


def test_commit_order_request(server_protocol: CafeProtocolServer,
                              mock_handler: Mock,
                              mock_io: MockCafeIO):
    # This test should set the mock_io.request_string to a legitimate COMMIT request
    # and then call server_protocol.receive_next_request. It should then confirm that
    # the handler's handle_commit_order was called with the same string that was
    # specified in the COMMIT request
    assert False        # remove this line when implementing the test


def test_commit_order_request_with_no_token(server_protocol: CafeProtocolServer,
                                            mock_handler: Mock,
                                            mock_io: MockCafeIO):
    # The protocol says that the COMMIT request message should include a settlement
    # token (any sequence of non-whitespace characters). If it receives a request
    # with no token, it should send an ERROR response, without calling the handler's
    # `handle_commit_order` method.
    assert False        # remove this line when implementing the test


def test_list_menu_request(server_protocol: CafeProtocolServer, mock_handler: Mock, mock_io: MockCafeIO):
    mock_io.request_string = "LIST MENU"
    server_protocol.receive_next_request()
    mock_handler.handle_list_menu.assert_called_once()


def test_list_order_request(server_protocol: CafeProtocolServer, mock_handler: Mock, mock_io: MockCafeIO):
    # Using the previous `test_list_menu_request` test function as a guide,
    # implement a simple test for the LIST ORDER request.
    assert False        # remove this line when implementing the test


def test_send_add_item_response(server_protocol: CafeProtocolServer, mock_io: MockCafeIO):
    # When we call server_protocol.send_add_item_response, we pass it the
    # number of items in the order. It should send an OK response followed by a message
    # that contains the number of items in the order.
    server_protocol.send_add_item_response(42)
    assert len(mock_io.response_strings) > 0
    assert mock_io.response_strings[0].startswith("OK ")
    assert "42" in mock_io.response_strings[0]


def test_send_remove_item_response(server_protocol: CafeProtocolServer, mock_io: MockCafeIO):
    # When we call server_protocol.send_remove_item_response, we pass it the item number
    # to remove. It should send an OK response followed by a message the includes the
    # item number. Using the `test_send_add_item_response` function as a guide, implement
    # this test case for the REMOVE item response.
    assert False        # remove this line when implementing the test


def test_send_cancel_item_response(server_protocol: CafeProtocolServer, mock_io: MockCafeIO):
    # A call to server_protocol.send_cancel_order_response should produce a response
    # message that starts with "OK " followed by an informational message. Using other test
    # cases as a guide, implement this test case for the cancel order response.
    assert False        # remove this line when implementing the test


def test_send_commit_item_response(server_protocol: CafeProtocolServer, mock_io: MockCafeIO):
    # A call to server_protocol.send_commit_order_response should produce a response
    # message that starts with "OK " followed by the order number passed as an argument.
    # Using other test cases as a guide, implement this test case for the cancel order response.
    assert False        # remove this line when implementing the test


def test_send_list_menu_response(server_protocol: CafeProtocolServer, mock_io: MockCafeIO):
    # A call to server_protocol.send_list_menu_response gets a list of menu item
    # names as an argument. It should produce sequence of strings, starting with a string
    # that starts with "OK" and the number of items that follow. The remaining strings start
    # with a non-negative integer representing the index into the list of items, followed
    # by the name of the menu item. See the lecture 1 slides for an example.
    #
    # Our test case simply provides a short list of menu item names to the call to the
    # `send_list_menu_response` method, and confirms that the strings in the generated
    # response are a match for the menu items we passed to it.
    server_protocol.send_menu_items_response(["Cheeseburger", "Chips", "Water"])
    assert len(mock_io.response_strings) == 4
    assert mock_io.response_strings[0] == "OK 3"
    assert mock_io.response_strings[1] == "0 Cheeseburger"
    assert mock_io.response_strings[2] == "1 Chips"
    assert mock_io.response_strings[3] == "2 Water"


def test_send_list_order_response(server_protocol: CafeProtocolServer, mock_io: MockCafeIO):
    # A call to server_protocol.send_list_order_response gets a list of item numbers as an
    # argument. It should produce sequence of strings, starting with a string
    # that starts with "OK" and the number of items that follow. The remaining strings start
    # with a non-negative integer representing the index into the list of items, followed
    # by a non-negative integer representing an ordered menu item. See the lecture 1 slides
    # for an example.
    #
    # Your test case should provides a short list of menu item numbers to the call to the
    # `send_list_order_response` method, and confirm that the strings in the generated
    # response are a match for the menu items we passed to it. Use the `test_send_list_menu_response`
    # test case as a guide to implement this test case.
    assert False        # remove this line when implementing the test