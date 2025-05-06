# Import sys module for modifying Python's runtime environment
import sys
# Import os module for interacting with the operating system
import os

import pytest
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arnotts_item import arnotts_item
from arnotts_user import arnotts_user
from vouchervault import app
from vouchervault import arnotts_json_to_order
@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client
            
def test_order_process(client):
    response = client.post("/arnotts", json= {
   "cart":{"items":[{"link":"https://www.arnotts.ie/men/clothing/coats-jackets/carhartt-wip/harvey-denim-overshirt/183168884.html?cgid=shop-by-department-men-clothing-coats-jackets","size":"0102, M","quantity":"3"}]},"user":{"email":"Radnitzoriasotie@gmail.com","title":"Mr","firstName":"Radnitz","lastName":"Oriasotie","phoneNumber":"+353899615828","country":"Ireland","addrLine1":"123 Example Street","addrLine2":"Example Town","townCity":"Dublin","county":"Dublin","eircode":"D12E45","delivery":["delivery"]}
        })
    
    assert response.get_data() == b'Success' 

def test_json_to_cart():
    cart_test : list[arnotts_item] = []
    user_test = arnotts_user("Radnitzoriasotie@gmail.com", "Mr", "Radnitz","Oriasotie","+353899615828","Ireland", "123 Example Street","Example Town","Dublin","Dublin","D12E45",['delivery'])
    cart_test.append(arnotts_item('https://www.arnotts.ie/men/clothing/coats-jackets/carhartt-wip/harvey-denim-overshirt/183168884.html?cgid=shop-by-department-men-clothing-coats-jackets', '3', 'M'))
    
    cart, user = arnotts_json_to_order({"cart":{"items":[{"link":"https://www.arnotts.ie/men/clothing/coats-jackets/carhartt-wip/harvey-denim-overshirt/183168884.html?cgid=shop-by-department-men-clothing-coats-jackets","size":"0102, M","quantity":"3"}]},"user":{"email":"Radnitzoriasotie@gmail.com","title":"Mr","firstName":"Radnitz","lastName":"Oriasotie","phoneNumber":"+353899615828","country":"Ireland","addrLine1":"123 Example Street","addrLine2":"Example Town","townCity":"Dublin","county":"Dublin","eircode":"D12E45","delivery":["delivery"]}}) 
    assert cart == cart_test, user==user_test
    