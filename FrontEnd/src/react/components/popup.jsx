import { Card, Button } from "@chakra-ui/react";
import { ChakraProvider } from '@chakra-ui/react';

let old_total = "10.00"
let new_total = "0.00"
let saving_percent = "5"

const onClick = () =>{
    
window.addEventListener("load", function(event) {
    setTimeout(function() {
          
        
        console.log("loaded")
        let goodsLinks = document.getElementsByClassName("shopingProductCard__name")

        let goodsSizes = document.getElementsByClassName("shopingProductCard__size")
        function Basket(items){
            this.items = items

        }

        let cart = new Basket([]);

        function Item(link, size){
            this.link = link
            this.size = size
        }

        console.log(goodsLinks.length)

        for (let i = 0; i < goodsLinks.length; i++){
            console.log(i)
            cart.items.push(new Item(goodsLinks[i].href, goodsSizes[i].innerHTML))

        }

        console.log(JSON.stringify(cart))
        
        fetch('http://127.0.0.1:5000/arnotts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(cart)
        })
    }, 2500);
});



}
const Popup = () => {
    return (
        <Card.Root width="sm">
        <Card.Body gap="2">
          <Card.Title mt="2">VoucherVault</Card.Title>
          <Card.Description>
            Save {saving_percent}% on your order by checking out using VoucherVault.
            {old_total.strike()} {new_total}
          </Card.Description>
        </Card.Body>
        <Card.Footer justifyContent="flex-end">
          <Button variant="outline">Close</Button>
          <Button onclick = {onClick} >CheckOut</Button>
        </Card.Footer>
      </Card.Root>
    )
}

export default Popup   