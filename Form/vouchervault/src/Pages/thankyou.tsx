import { Heading, Flex, Text} from "@chakra-ui/react";

function ThankYou(){
return(
        
    <Flex
    wrap="wrap"
    maxW="2000px"
    justify="center"
    align="center"
    direction="column"
    
    
  >
    <Heading size="7xl" color="#354ead"> VoucherVault </Heading>
    <Text padding={150} textStyle="2xl" fontWeight="semibold" letterSpacing="tight" justifyContent="center" mt="2">
    Your order has been placed. Thank you for using VoucherVault. You will recieve an email shortly.
    </Text>
    </Flex>
    
    )
}
export default ThankYou