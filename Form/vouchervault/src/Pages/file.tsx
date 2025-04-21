//Return user details in header encoded in base64.
import { Button, Card, Flex, Heading, Input, Field, Text, Center, Select, Portal, createListCollection} from '@chakra-ui/react'
import {SyntheticEvent, useState} from 'react'

/**
 * Component for form page
 * @returns FormFill, the form page.
 */
function FormFill(){
    //Various user details.
    const [Email, setEmail] = useState('')
    const [Title, setTitle] = useState('')
    const [FirstName, setFirstName] = useState('')
    const [LastName, setLastName] = useState('')
    const [PhoneNumber, setPhoneNumber] = useState('')
    const [Country, setCountry] = useState('')
    const [AddrLine1, setAddrLine1] = useState('')
    const [AddrLine2, setAddrLine2] = useState('')
    const [TownCity, setTownCity] = useState('')
    const [County, setCounty] = useState('')
    const [Eircode, setEircode] = useState('')
    const [Delivery, setDelivery] = useState<string[]>([])
    //Gets URL Params from current page
    const urlParams = new URLSearchParams(window.location.search);

    //Old price, new price

    let oldPrice: string | null = urlParams.get('price')
    let newPrice = 0

    if (oldPrice != null){
        newPrice = (+oldPrice * 0.95)
    }
    

        /**
         * Function that runs when the form is submitted.
         * @param e 
         */
    const submitForm = (e: SyntheticEvent) =>{
        e.preventDefault()
        
        let nullable_cart: string | null = urlParams.get('cart');
        let cart = ""
        if (nullable_cart != null){
            cart = atob(nullable_cart)
        }
        
        const user_details: { email: string; title: string; firstName: string, lastName: string, phoneNumber: string, country:string, addrLine1: string, addrLine2: string, townCity: string, county: string, eircode: string, delivery: string[]} = {
            email: Email,
            title: Title,
            firstName: FirstName,
            lastName: LastName,
            phoneNumber: PhoneNumber,
            country: Country,
            addrLine1: AddrLine1,
            addrLine2: AddrLine2,
            townCity: TownCity,
            county: County,
            eircode: Eircode,
            delivery: Delivery

        }

        cart = JSON.parse(cart)
        let arnotts_order = {
            cart,
            user: user_details
        }


        
        fetch('http://127.0.0.1:5000/arnotts', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(arnotts_order)
        }).then((res) => {
            if(res.ok){
            console.log("Sent Details.");}
            else{
                console.log("Failed to send details.");
            }
        })

        //location.href="/order-placed"
    }


    

    return(
        
        <Flex
        wrap="wrap"
        maxW="2000px"
        justify="center"
        align="center"
        direction="column"
        paddingY={20}
        
      >
        <Heading size="7xl" color="#354ead"> VoucherVault </Heading>
        
        <form onSubmit={submitForm}>

                        <Field.Root required>            
                            <Field.Label>
                                Email <Field.RequiredIndicator />
                            </Field.Label>  
                            <Input placeholder="me@example.com" variant="flushed" width="500px" onChange = {e => setEmail(e.target.value)} />
                        </Field.Root>  
                        <Field.Root required>
                            <Field.Label>
                                Title <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="Mr. Mrs etc" width="500px" variant="flushed" onChange = {e => setTitle(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                First Name <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="First" variant="flushed" onChange = {e => setFirstName(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                Last Name <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="Last" variant="flushed" onChange = {e => setLastName(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                Phone Number <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="+35312345678" variant="flushed" onChange = {e => setPhoneNumber(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                Country  <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="Ireland" variant="flushed" onChange = {e => setCountry(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                Address Line 1  <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="Address Line 1" variant="flushed" onChange = {e => setAddrLine1(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                Address Line 2  <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="Address Line 2" variant="flushed" onChange = {e => setAddrLine2(e.target.value)} />
                        </Field.Root>
                        <Select.Root  collection={deliveryOpts} size="md" width="500px" paddingY={5} value={Delivery} onValueChange={(e) => setDelivery(e.value)}>
                        <Select.HiddenSelect />
                        <Select.Control>
                            <Select.Trigger>
                            <Select.ValueText placeholder="Shipping" />
                            </Select.Trigger>
                            <Select.IndicatorGroup>
                            <Select.Indicator />
                            </Select.IndicatorGroup>
                        </Select.Control>
                        <Portal>
                            <Select.Positioner>
                            <Select.Content>
                                {deliveryOpts.items.map((deliveryOpts: any) => (
                                <Select.Item item={deliveryOpts} key={deliveryOpts.value}>
                                    {deliveryOpts.label}
                                    <Select.ItemIndicator />
                                </Select.Item>
                                ))}
                            </Select.Content>
                            </Select.Positioner>
                        </Portal>
                        </Select.Root>
                        <Field.Root required>
                            <Field.Label>
                                Town/City  <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="Dublin" variant="flushed" onChange = {e => setTownCity(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                County  <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="Dublin" variant="flushed" onChange = {e => setCounty(e.target.value)} />
                        </Field.Root>
                        <Field.Root required>
                            <Field.Label>
                                Eircode  <Field.RequiredIndicator />
                            </Field.Label>
                            <Input placeholder="D12EF45" variant="flushed" onChange = {e => setEircode(e.target.value)} />
                        </Field.Root>
                        <Center paddingY={20}>
                        
                        <Card.Root maxW="sm" overflow="hidden" >
                        <Card.Body gap="2">
                            <Card.Title>Checkout using VoucherVault</Card.Title>
                            <Card.Description>
                            Get 5% off when checking out with VoucherVault.
                            </Card.Description>
                            <Text textStyle="3xl" fontWeight="light" letterSpacing="tight" justifyContent="center" mt="2">
                            <span><del>€{oldPrice}</del></span>      
                            </Text>
                            <Text textStyle="1xl" fontWeight="light" letterSpacing="tight" justifyContent="center" mt="2">
                            <span>incl. shipping (€5.95)</span>      
                            </Text>
                            <Text textStyle="4xl" fontWeight="bold" letterSpacing="tight" justifyContent="center" mt="2">
                             €{String(newPrice.toFixed(2))}
                            </Text>
                            <Text textStyle="1xl" fontWeight="light" letterSpacing="tight" justifyContent="center" mt="2">
                            <span>incl. shipping (€5.95)</span>      
                            </Text>
                        </Card.Body>
                        <Card.Footer gap="2">
                            <Button variant="outline" type="submit">Pay with Stripe</Button>
                        </Card.Footer>
                        </Card.Root>
                        </Center>     
                    </form>
                
                </Flex>
    )



}

const deliveryOpts = createListCollection({
    items: [
      { label: "Click And Collect: €0.00", value: "free" },
      { label: "Delivery:  €5.95", value: "delivery" },
    ],
  })

export default FormFill;