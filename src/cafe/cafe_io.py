from abc import ABC, abstractmethod


class CafeIO(ABC):
    """
    An abstract representation of a communication channel that can send and receive
    strings. A typical implementation will communicate via a stream or socket.
    """

    @abstractmethod
    def read_string(self) -> str:
        """
        Reads a non-empty string representing a line of text from the input source. A line
        is a sequence of printing characters terminated by a newline.
        The returned string MUST have no leading or trailing whitespace (including newline)
        :return: a non-empty string with leading and trailing whitespace removed
        """
        pass

    @abstractmethod
    def write_string(self, s: str):
        """
        Writes the given string to the output sink as a line of text. The string will be
        followed by a newline on output
        :param s: is the string to write; must consist only of printing characters
        :return: None
        :raises: ValueError if `s` is None or an empty string
        """
        pass

