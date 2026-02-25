
from cafe import CafeIO, CafeOrderHandler, CafeProtocolServer, CafeService


class SimpleCafeOrderHandler(CafeOrderHandler):

    def __init__(self, cafe_client: CafeIO, cafe_service: CafeService):
        self._client = cafe_client
        self._service = cafe_service
        self._interpreter: CafeProtocolServer = None
        self._menu_items = cafe_service.menu_items()
        self._ordered_items: list[int] = []
        self._done = False

    def handle_list_menu(self):
        self._interpreter.send_menu_items_response(self._menu_items)

    def handle_list_order(self):
        self._interpreter.send_order_items_response(self._ordered_items)

    def handle_add_item(self, item_number: int):
        if item_number < len(self._menu_items):
            self._ordered_items.append(item_number)
            self._interpreter.send_add_item_response(len(self._ordered_items))
        else:
            self._interpreter.send_error_response(f"menu item {item_number} does not exist")

    def handle_remove_item(self, item_number: int):
        if item_number < len(self._ordered_items):
            self._ordered_items.pop(item_number)
            self._interpreter.send_remove_item_response(item_number)
        else:
            self._interpreter.send_error_response(f"order item {item_number} does not exist")

    def handle_commit_order(self, settlement_token: str):
        order_number = self._service.place_order(settlement_token, self._ordered_items)
        self._done = True
        self._interpreter.send_commit_order_response(order_number)

    def handle_cancel_order(self):
        self._done = True
        self._interpreter.send_cancel_order_response()

    def serve_client(self):
        # if done is true, this order has already been committed or canceled
        if self._done:
            raise RuntimeError("order handlers cannot be reused")
        self._interpreter = CafeProtocolServer(self, self._client)
        while not self._done:
            self._interpreter.receive_next_request()

