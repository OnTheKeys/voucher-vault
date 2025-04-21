from item import item

class arnotts_item(item):
    """A class to represent an item from the Arnotts store.

    Args:
        item (item): The abstract item class.
    """
    def __init__(self, link: str, quantity: int, size: str):
        """Creates an instance of the arnotts item class.

        Args:
            link (str): A link to the Arnotts item to be purchased.
            quantity (int): The quantity of the Arnotts item to be purchased.
            size (str): The size of the item to be purchased. It can be be a number e.g "36" or a string of numbers and letters e.g "2XL".
        """
        super().__init__(link, quantity)
        self.size = size