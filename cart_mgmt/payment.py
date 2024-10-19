from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.create_order_request import CreateOrderRequest
import time


from cashfree_pg.models.order_meta import OrderMeta

# Inside your function, after creating customer_details



def process_cashfree_payment(amount, user):
    """
    Process payment using Cashfree PG API by creating an order.

    Args:
        amount (float): The amount to be charged.
        user: The user making the payment.

    Returns:
        bool: True if payment session is created successfully, False otherwise.
    """
    try:
        # Set Cashfree credentials
        Cashfree.XClientId = "TEST10331725b4ea117d6a191844b7b052713301"
        Cashfree.XClientSecret = "cfsk_ma_test_753a7ae29e7c38626f7f5caa5b20d26c_652187ae"
        Cashfree.XEnvironment = Cashfree.SANDBOX

        # Generate order ID
        order_id = f"{user.id}_{int(time.time())}"[:45]

        # Create customer details
        customer_details = CustomerDetails(
            customer_id=str(user.id),
            customer_name=user.firstname,
            customer_email=user.email,
            customer_phone=user.mobilenumber
        )


        order_meta = OrderMeta(
        return_url="https://google.com/",  # Ensure this is a valid URL
        notify_url="https://your-notify-url.com/",  # Include if required
        payment_methods=["DEBIT_CARD"]  # Adjust as necessary
        )

        # Create order request
        create_order_request = CreateOrderRequest(
            order_id=order_id,
            order_amount=amount,  # Make sure this is a float or integer
            order_currency="INR",  # Use correct currency code
            return_url="https://google.com/",  # Your return URL
            customer_details=customer_details,
            order_meta=order_meta
        )

        # Set the API version
        api_version = "2023-08-01"  # Use a valid version

        # Create the order
        response = Cashfree.PGCreateOrder(
            x_api_version=api_version,
            create_order_request=create_order_request
        )

        # Check response status
        if response.status == 'OK':
            payment_session_id = response.payment_session_id
            print(f"Order created successfully! Payment session ID: {payment_session_id}")
            return True
        else:
            print(f"Order creation failed: {response.message}")
            return False

    except Exception as e:
        print(f"Payment processing error: {e}")
        return False

