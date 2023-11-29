# Anvi-Bot-A

Anvi-Bot-A - this is a Telegram-bot of the "Fluffy wildebeest" team for purchasing cosmetics from the site `https://anvibodycare.com`

# Features
- ready to deploying Heroku
- item status in short discription  
- posability redirect to checkout page(only one item in bot cart)
- manual update catalog.json in bot
- all data is updated once a day at `06:00` Kyiv time

<!---- logging to https://papertrail.com - variations items for "Hair" category --->
...
---
### Get the repository
Clone the repository -> navigate to the cloned folder -> install `requirments.txt`:
```sh
git clone https://github.com/bassdarkside/Anvi-Bot-A.git
cd Anvi-Bot-A
pip install -r requirments.txt
```
---
## Before you start  
Create `.env` file in `/Anvi-Bot-A` dirctory.  
```sh
touch ~/Anvi-Bot-A/.env
```
Open `.env` and put Telegram API KEY, Telegram user ID.  
```
TOKEN = "YOUR_API_KEY"
ADMIN = your_id
```
<!--- 

>**Listen Chat** _<https://t.me/+loCzklVYXz5hOTJi>_.
![how to](img/how-to-env.png?raw=true "Title") -->


## Start the bot
Run in command line:
```sh
python run.py
```

## In Telegram Bot

### Admin can check current update data schedule with command  :
    /status  

### Start manual update only `catalog.json` with command:
    /update
### Send command to get description:
    /admin

# How to add multiple products to cart WooCommerce via URL

WooCommerce provides you with the ability to do practically anything. Creating a custom link to add multiple things to the cart is part of this.  
Refer to the process below to learn how to add multple products to cart WooCommerce via URL.

#### Step 1: Create and copy the function code

Below is the code you will use to create the product URL. Just copy it and we will paste it into your child theme’s `functions.php` file.
```php
function webroom_add_multiple_products_to_cart( $url = false ) {
    // Make sure WC is installed, and add-to-cart qauery arg exists, and contains at least one comma.
        if ( ! class_exists( 'WC_Form_Handler' ) || empty( $_REQUEST['add-to-cart'] ) || false === strpos( $_REQUEST['add-to-cart'], ',' ) ) {
                return;
        }

    // Remove WooCommerce's hook, as it's useless (doesn't handle multiple products).
        remove_action( 'wp_loaded', array( 'WC_Form_Handler', 'add_to_cart_action' ), 20 );

        $product_ids = explode( ',', $_REQUEST['add-to-cart'] );
        $count       = count( $product_ids );
        $number      = 0;

        foreach ( $product_ids as $id_and_quantity ) {
// Check for quantities defined in curie notation (<product_id>:<product_quantity>)

                $id_and_quantity = explode( ':', $id_and_quantity );
                $product_id = $id_and_quantity[0];

                $_REQUEST['quantity'] = ! empty( $id_and_quantity[1] ) ? absint( $id_and_quantity[1] ) : 1;

                if ( ++$number === $count ) {
// Ok, final item, let's send it back to woocommerce's add_to_cart_action method for handling.
                        $_REQUEST['add-to-cart'] = $product_id;

                        return WC_Form_Handler::add_to_cart_action( $url );
                }

                $product_id        = apply_filters( 'woocommerce_add_to_cart_product_id', absint( $product_id ) );
                $was_added_to_cart = false;
                $adding_to_cart    = wc_get_product( $product_id );

                if ( ! $adding_to_cart ) {
                        continue;
                }

                $add_to_cart_handler = apply_filters( 'woocommerce_add_to_cart_handler', $adding_to_cart->get_type(), $adding_to_cart );

// Variable product handling
                if ( 'variable' === $add_to_cart_handler ) {
                        woo_hack_invoke_private_method( 'WC_Form_Handler', 'add_to_cart_handler_variable', $product_id );

// Grouped Products
                } elseif ( 'grouped' === $add_to_cart_handler ) {
                        woo_hack_invoke_private_method( 'WC_Form_Handler', 'add_to_cart_handler_grouped', $product_id );

// Custom Handler
                } elseif ( has_action( 'woocommerce_add_to_cart_handler_' . $add_to_cart_handler ) ){
                        do_action( 'woocommerce_add_to_cart_handler_' . $add_to_cart_handler, $url );

// Simple Products
                } else {
                        woo_hack_invoke_private_method( 'WC_Form_Handler', 'add_to_cart_handler_simple', $product_id );
                }
        }
}

// Fire before the WC_Form_Handler::add_to_cart_action callback.
add_action( 'wp_loaded', 'webroom_add_multiple_products_to_cart', 15 );

/**
 * Invoke class private method
 *
 * @since   0.1.0
 *
 * @param   string $class_name
 * @param   string $methodName
 *
 * @return  mixed
 */
function woo_hack_invoke_private_method( $class_name, $methodName ) {
        if ( version_compare( phpversion(), '5.3', '<' ) ) {
                throw new Exception( 'PHP version does not support ReflectionClass::setAccessible()', __LINE__ );
        }

        $args = func_get_args();
        unset( $args[0], $args[1] );
        $reflection = new ReflectionClass( $class_name );
        $method = $reflection->getMethod( $methodName );
        $method->setAccessible( true );

//$args = array_merge( array( $class_name ), $args );
        $args = array_merge( array( $reflection ), $args );
        return call_user_func_array( array( $method, 'invoke' ), $args );
}
```

#### Step 2: Edit theme functions.php file

Before making any changes to the Theme File `functions.php` file, you should create a child theme and activate it instead of the main one. This will help you avoid the unexpected issues happening to your main theme.

*   To get access to the functions.php file, from your WooCommerce dashboard, you should go to **Appearance > Theme File Editor.**  
![how to](img/19.png?raw=true "Title")

*   Paste the code you have copied in the first step in the code editing area   

    ![how to](img/20.png?raw=true "Title")

*   Hit the **Update File** button.

#### Step 3: Preview and check

It’s time to see and test the result. You should visit your WooCommerce store front-end and click on a single product page. Your single product URL for adding multiple products to the shopping cart will look like this:

    https://www.example.com/cart/?add-to-cart=12345,43453

As you can see in the **?add-to-cart=12345,43453** part where you add your product ids. If you want to add 2 items of the same product, just type twice its product id:

    https://www.example.com/cart/?add-to-cart=12345,12345,12345

How to get the product ID? You can find the product’s ID by navigating to **Products > All Products** from your WooCommerce dashboard, then hovering the mouse over the product you want to buy. The product ID is under the product name as in the picture below.

![how to get the product ID](img/21.png?raw=true "Title")

Or you can add the following string: `&quantity=3` in the last part of the URL. The result you can get will look like this:

    https://www.example.com/cart/?add-to-cart=12345&quantity=3
Source - https://woostify.com/add-multiple-products-to-cart-woocommerce/
