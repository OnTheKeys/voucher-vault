from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains 
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from contextlib import suppress
import logging
from threading import Event, Lock
import os

from flask import Flask, request
from flask_cors import CORS
from arnotts_item import arnotts_item
from arnotts_user import arnotts_user
import time
import re
from multiprocessing import Process, cpu_count

#Selenium Browser Driver setup.

PATH = Service(os.environ['PATH_TO_DRIVER'])
options = Options()
options.binary_location = os.environ['PATH_TO_BINARY']

#Multithreading driver event and lock setup
driver_free = Event()
driver_free.set()
driver_lock = Lock()


class Driver():
    def __new__(cls):
        with driver_lock:
            if not hasattr(cls, 'instance'):
                cls.instance = webdriver.Firefox(service=PATH, options=options)
        return cls.instance
            

#Flask Setup.
app = Flask(__name__)
CORS(app)
#Misc setup.
logger = logging.getLogger(__name__)
"""
Group of functions that make the repeated use of specific time sleep values slightly more intuitive to read
"""
def short_pause():
    time.sleep(1)
    
def medium_pause():
    time.sleep(3)
def long_pause():
    time.sleep(7)
    
def alternative_click(driver, element: WebElement):
    """A function for using the alternative method of clicking in selenium. 
        Useful if the main method of clicking doesnt work.
    Args:
        driver (WebDriver): The web driver the element is being clicked in.
        element (WebElement): The element to be clicked.
    """
    driver.execute_script("arguments[0].click();", element)
def offset_scroll(driver, value =240, multiplier=-1):
    """The element locations on the Arnotts website seem to be offset on the Y axis. 
    This function helps scroll against this offset, fixing an error where the element scrolled to is not on screen.
    Args:
        driver (WebDriver): The driver the scrolling is happening in.
        value (int, optional): The amount to be scrolled in the Y direction. Defaults to 240.
        multiplier (int, optional): The amount the scroll is multipled by, The sign changes direction. Defaults to -1.
    """
    try:
        ActionChains(driver)\
        .scroll_by_amount(0, multiplier *  value)\
        .perform()
        short_pause()
    except IndexError as e:
        logger.error(f"Invalid coordinates: {e}")
        
def handle_arnotts_button(wait: WebDriverWait):
    """Function to handle the cookies button that pops up when the storefront is first visited.
    
    Args:
        wait (WebDriverWait) Takes in a WebDriverWait object.
    """
    #Necessary wait time to deal with the button loading and popping up
    long_pause()
    try:
        element = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        element.click()
    except AttributeError as e: 
        logger.error(f"Button not found: {e}")
    
def match_size(item: arnotts_item, size: WebElement, driver):
    """Function to match the size of an item with a given size on the website.
    Args:
        item (arnotts_item): The item with a size to be matched.
        size (WebElement): A dropdown WebElement containing a size.
        driver (WebDriver): The web driver the function should run using.
    Returns:
        Boolean: True if size matches, false if it does not.
    """
    #The text of the size HTML element is accessed.
    #The split with a new line delimeter fixes an issue with low stock Arnotts sizes which are suffexed by "\nLOW STOCK"
    first_line = size.text.split('\n')[0]
    #The first line of the size name is then stripped of all letters and converted to only numbers. 
    #The format of sizes on the Arnotts website guarantees numbers at the end of the first line.
    stripped_numbers = re.sub('[a-zA-Z]', '' ,first_line).split(' ')[-1]
    #The size given by the item is compared to the size present in the WebElement using various methods
    #First the raw text of both is compared, 
    #Then the raw text present in the split using a space as a delimeter and stripped of its brackets before being compared
    #The above approach is useful for comparing something like M to EU (M) as is common on Arnotts.
    #The items size is then compared to the first line we got earlier and finally just the numbers provided by the web element.
    if item.size == size.text or item.size == size.text.split(' ')[-1].strip("()") or item.size == first_line or item.size == stripped_numbers:
        #Scrolls to the location of the matched size Web Element.
        size.location_once_scrolled_into_view
        #Short pause to complete scroll.
        short_pause()
        offset_scroll(driver)
        size.click()
        return True
    return False
def find_sizes(driver):
    """Function that retrieves all possible sizes for an certain on screen item from the Arnotts website.
    Args:
        driver (WebDriver): The web driver the sizes are to be found in.
    Returns:
        list [WebElement]: Returns a list of the available sizes in strings.
    """
    #Arnotts handles sizes in its dropdown menu by labelling them as dropdownSizeValueN 
    #where N starts at 0 and goes up to the number of sizes available.
    base_string = "dropdownSizeValue"
    dropdowns = []
    i = 0
    #While the dropdownSizeValueN is available append its webElement to the list of available sizes.
    while driver.find_elements(By.ID, base_string+str(i)):
        dropdowns.append(driver.find_elements(By.ID, base_string+str(i))[0])
        i+=1
        
    return dropdowns
def get_giftcard():
    """Incomplete function. 
    Would fetch an apprproiate gift card from the database if we had giftcards to store.
    Returns:
        gift_card(str): Gift card number as string. Hardcoded for now.
    """
    gift_card = "12345678910"
    return gift_card
def enter_user_details_arnotts(driver, user: arnotts_user):
    """Takes in a driver and a user then fills the user's details into the arnotts form
    Args:
        driver (WebDriver): The web driver in use.
        user (arnotts_user): The user object the details will be extracted from.
    """
    dropdown = driver.find_element(By.NAME, "title")
    dropdown.find_element(By.XPATH, f"//option[. = '{user.title}']").click()
    driver.find_element(By.NAME, "fname").send_keys(user.first_name)
    driver.find_element(By.NAME, "lname").send_keys(user.last_name)
    driver.find_element(By.NAME, "phone").send_keys(user.phone_number)
    dropdown = driver.find_element(By.NAME, "country")
    dropdown.find_element(By.XPATH, f"//option[. = '{user.country}']").click()
    driver.find_element(By.NAME, "address1").send_keys(user.addr_line1)
    driver.find_element(By.NAME, "address2").send_keys(user.addr_line2)
    driver.find_element(By.NAME, "town").send_keys(user.town_city)
    dropdown = driver.find_element(By.NAME, "county")
    dropdown.find_element(By.XPATH, f"//option[. = '{user.county}']").click()
    driver.find_element(By.NAME, "postcode").send_keys(user.eircode)
    short_pause()
    
def arnotts_order(cart : list [arnotts_item], user : arnotts_user):
    """A function that places an order on the Arnotts Website
    Args:
        cart (list [arnotts_item]): A list of arnotts items to be ordered.
        user (arnotts_user): The Arnotts user the items are ordered for.
    """
    #Initliazises the driver if it has not already been initialized
    
    driver = Driver()
    #Thread waits until the driver is free and then clears the driver free flag.
    #letting other threads know the driver is unavailable.
    driver_free.wait()
    driver_free.clear()
    
    #Defines a long wait time for the driver. 
    #This gives the driver what is essentially a timeout waiting for an event.
    long_wait = WebDriverWait(driver, 10)
    
    for i, item in enumerate(cart):
        #Navigates to the webpage of the item
        driver.get(item.link)
        
        #Handles the cookies button if this is the first arnotts page visited.
        #If it never shows up and the time set to wait times out the process continues
        if i == 0:
            with suppress(TimeoutException):
                handle_arnotts_button(long_wait)
        
        #Wait for the size selection button to be clickable after handling cookie button.
        #Then scroll to the "location" of the size button.     
        element = long_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "size-name  ")))
        element.location_once_scrolled_into_view
        
        #A medium pause to allow the scrolling to be completed
        medium_pause()
        #The element location on the arnotts website seems to be offset so scroll back up in the opposite direction.
        offset_scroll(driver)
        
        driver.find_element(By.CSS_SELECTOR, ".pdp-product-selectors .size-name").click()
        #Create a list of all possible sizes
        sizes = find_sizes(driver)
        
        #Attempts to match the rquested size to one of the available options.
        size_index=0
        size = sizes[size_index]
        while not match_size(item, size, driver):
            try:
                size_index+=1
                size = sizes[size_index]
            except IndexError as e:
                return f"Failed. Size not found.: {e}", 400 
        
        #Change item quantity to quantity specified by user.  
        for _ in range(1, int(item.quantity)):
            driver.find_element(By.CSS_SELECTOR, ".add-qty").click()
        
        #Adds item to cart.
        element= driver.find_element(By.CLASS_NAME, "addToBagLoader")
        ActionChains(driver)\
        .scroll_to_element(element)\
        .perform()
        #The regular selenium click causes an error with this button so it must be clicked alternatiely.
        alternative_click(driver, element)
        #Short pause to process the order.
        medium_pause()
    
    driver.get("https://www.arnotts.ie/checkoutlogin/")
    #Short wait to load the checkoutlogin page.
    medium_pause()
    #Enters the users email and clicks the button to start the guest checkout process.
    driver.find_element(By.ID, "guestemail").send_keys(user.email)
    driver.find_element(By.CSS_SELECTOR, ".guestCta").click()
    #Medium sized pause to allow the page to load
    long_pause()
    
    #Fill in all the user's details.
    enter_user_details_arnotts(driver, user)
    offset_scroll(driver, 250, 1)
    
    #Waits until the button to proceed to the next step is clickable before using the alt click on it,
    element = long_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nextStep")))
    short_pause()
    alternative_click(driver, element)
    #Repositions to access the button for the next part of the process.
    offset_scroll(driver, 250, 1)
    #Uses the alternative click to proceed to the next part of the payment process.
    element = driver.find_element(By.CSS_SELECTOR, ".upnext_button")
    alternative_click(driver, element)
    #This pause allows the payment section to appear on screen.
    medium_pause()
    #Enter gift card into pay with gift card field.
    driver.find_element(By.CSS_SELECTOR, ".paygiftcard__textfield").send_keys(get_giftcard())
    
    #Signals driver is free again before returning.
    driver_free.set()
    return "Success", 200 


def arnotts_json_to_order(json):
    cart = []
        #Filling in cart details. 
    for line in json['cart']['items']:
        item = arnotts_item(line['link'], line['quantity'], line['size'].split(',')[-1].strip())
        cart.append(item)
    
    #Filling in user details.
    user_details = json['user']
    user = arnotts_user(user_details["email"], user_details["title"], user_details["firstName"], user_details["lastName"], user_details["phoneNumber"], user_details["country"], user_details["addrLine1"], user_details["addrLine2"], user_details["townCity"], user_details["county"], user_details["eircode"], user_details['delivery'])
    print(cart)
    print(user)
    return cart, user
    
@app.route("/arnotts", methods=['POST', 'GET'])
def arnotts():
    """Function to handle creating a new WebDriver and ordering from arnotts when a request is recieved.
    Returns:
        HTTP Response: Response from arnotts_order function.
    """

    if request.method == 'POST':
        cart, user = arnotts_json_to_order(request.json)
    
    return arnotts_order(cart, user)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)







