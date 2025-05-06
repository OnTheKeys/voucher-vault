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
        
    def __eq__(self, other: object) -> bool:
        """Function to determine equality.

        Args:
            other (object): Object to be compared to.

        Returns:
            bool: True if equal, false otherwise.
        """
        if not isinstance(other, item):
            return False     
        return (self.link == other.link and self.quantity == other.quantity)
        