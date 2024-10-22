from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.models.order_meta import OrderMeta
import time
import os
from dotenv import load_dotenv

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
        load_dotenv()
        # Set Cashfree credentials
        Cashfree.XClientId = os.getenv('XClientId')
        Cashfree.XClientSecret = os.getenv('XClientSecret')
        Cashfree.XEnvironment = Cashfree.SANDBOX
        x_api_version = "2023-08-01"

        # Generate order ID
        order_id = f"{user.id}_{int(time.time())}"[:45]

        # Create customer details
        customer_details = CustomerDetails(
            customer_id=str(user.id),
            customer_phone=user.mobilenumber
        )

        # Create order meta
        order_meta = OrderMeta(
            return_url="https://google.com/",  # Ensure this is a valid URL
        )

        # Create order request
        create_order_request = CreateOrderRequest(
            order_id=order_id,
            order_amount=amount,  # Make sure this is a float or integer
            order_currency="INR",  # Use correct currency code
            customer_details=customer_details,
            order_meta=order_meta
        )

        # Create the order
        response = Cashfree().PGCreateOrder(
            x_api_version=x_api_version,
            create_order_request=create_order_request
        )

        # Check response status
        if hasattr(response, 'data'):
            order_data = response.data
            print(order_data)
            # Check the order status
            if order_data.order_status == 'ACTIVE':
                payment_session_id = order_data.payment_session_id
                print(f"Order created successfully! Payment session ID: {payment_session_id}")
                return True
            else:
                print(f"Order creation failed: {order_data.order_status}")
        else:
            print(f"Unexpected response structure: {response.__dict__}")
            if hasattr(response, 'error_code'):
                print(f"Error code: {response.error_code}")
            if hasattr(response, 'error_message'):
                print(f"Error message: {response.error_message}")

    except Exception as e:
        print(f"Payment processing error: {e}")
        return False

