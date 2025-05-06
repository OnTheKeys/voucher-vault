from abc import ABC

class user(ABC):
    """An abstract class to represent a user of VoucherVault.

    Args:
        ABC (_type_): Defines as abstract class.
    """
    def __init__(self, email: str, title: str, first_name: str, last_name: str, phone_number: str, country: str, addr_line1: str, addr_line2: str, town_city: str, county: str, eircode: str):
        """Creates an instance of the user class.

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
        """
        self.email = email 
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.country = country
        self.addr_line1 = addr_line1
        self.addr_line2 = addr_line2
        self.town_city = town_city
        self.county = county
        self.eircode = eircode
    
    def __eq__(self, other: object) -> bool:
        """Function to determine equality.

        Args:
            other (object): Object to be compared to.

        Returns:
            bool: True if equal, false otherwise.
        """
        if not isinstance(other, user):
            return False
        
        return (self.email == other.email and
            self.title == other.title and 
            self.first_name == other.first_name and 
            self.last_name == other.last_name and 
            self.phone_number == other.phone_number and
            self.country == other.country and 
            self.addr_line1 == other.addr_line1 and
            self.addr_line2 == other.addr_line2 and
            self.town_city == other.town_city and
            self.county == other.county and
            self.eircode == other.eircode)
                
            
    