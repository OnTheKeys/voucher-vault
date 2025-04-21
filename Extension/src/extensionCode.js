
chrome.runtime.onMessage.addListener(
     function(request, sender, sendResponse) {
        if( request.message === "start" ) {
            console.log("hi")
            const encoded_cart = onClick()
            sendResponse(encoded_cart)
        }
        return true;
    }

);

function onClick(){          
        
        console.log("loaded")
        let goodsLinks = document.getElementsByClassName("shopingProductCard__name")
        
        let goodsSizes = document.getElementsByClassName("shopingProductCard__size")

        let quantities = document.getElementsByClassName("quantity")

        let price = document.getElementsByClassName("orderSummary__value")[0].textContent.substring(1);

        
        console.log(price)
        function Basket(items){
            this.items = items        
        }

        let cart = new Basket([]);

        function Item(link, size, quantity){
            this.link = link
            this.size = size
            this.quantity = quantity
        }   
        console.log(goodsLinks.length)

        for (let i = 0; i < goodsLinks.length; i++){
            console.log(i)
            cart.items.push(new Item(goodsLinks[i].href, goodsSizes[i].innerHTML, quantities[i].textContent))

        }
        
        console.log(cart)
        return [btoa(JSON.stringify(cart)), price];

  
    }


