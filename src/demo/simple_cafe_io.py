from cafe import CafeIO

class SimpleCafeIO(CafeIO):
    """
    A simple implementation of `CafeIO` that communicates with a "client"
    via the keyboard and display.
    """

    def read_string(self) -> str:
        s = input().strip()
        while not s:
            s = input().strip()
        return s

    def write_string(self, s: str):
        print(s)


