from user import user

class arnotts_user(user):
    """A representation of a vouchervault user that is purchasing an item from arnotts.

    Args:
        user: The user abstract base class.
    """
    def __init__(self, email : str, title: str, first_name: str, last_name: str, phone_number: str, country: str, addr_line1: str, addr_line2: str, town_city: str, county: str, eircode: str, delivery: str):
        """Creates an instance of the arnotts user class.

        Args:
            email (str): The email of the user.
            title (str): The title of the user. e.g "Ms"
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            phone_number (str): The phone number of the user.
            country (str): The country the user resides in.
            addr_line1 (str): The first line of the user's address.
            addr_line2 (str): The second line of the user's address.
            town_city (str): The town or city the user's resides in.
            county (str): The county the user's resides in.
            eircode (str): The eircode of the user's address.
            delivery (str): The type of delivery selected by the user.
        """
        super().__init__(email, title, first_name, last_name, phone_number, country, addr_line1, addr_line2, town_city, county, eircode)
        self.delivery = delivery
        