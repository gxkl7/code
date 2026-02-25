
from cafe import CafeService
from .simple_cafe_io import SimpleCafeIO
from .simple_cafe_client_handler import SimpleCafeOrderHandler

_MENU_ITEMS = [
    "Hamburger",
    "Cheeseburger",
    "Chicken Wrap",
    "Veggie Wrap",
    "Chips",
    "Garden Salad",
    "Fountain Drink",
    "Water",
    "Iced Tea",
    "Coffee",
]

def run():
    # our fake fulfillment service simply has takes a list of menu options
    # and "fulfills" orders by printing them on the display
    cafe_service = CafeService(_MENU_ITEMS)
    # our fake client receives input from the keyboard and sends output to the display
    client = SimpleCafeIO()

    print("Waiting for request...")
    # handle the order interaction for our fake client
    handler = SimpleCafeOrderHandler(client, cafe_service)
    handler.serve_client()
