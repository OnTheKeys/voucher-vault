from abc import ABC

class item(ABC):
    """An abstract class to represent an item that can be purchased online.

    Args:
        ABC: Defines as abtract base class.
    """
    def __init__(self, link: str, quantity: int):
        """Constructs the item class.

        Args:
            link (string)): Alink to the item.
            quantity (int): Quantity of item to be purchased.
        """
        self.link = link
        self.quantity = quantity
        