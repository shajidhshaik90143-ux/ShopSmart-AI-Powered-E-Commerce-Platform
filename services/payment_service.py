import uuid


def process_payment(amount):

    """
    Demo online payment processor.

    This does NOT charge real money.
    It creates a simulated transaction ID.
    """

    if amount <= 0:

        return {

            "success": False,

            "method": "Online Payment",

            "transaction_id": None

        }


    transaction_id = (

        "PAY-"

        + uuid.uuid4()
        .hex[:12]
        .upper()

    )


    return {

        "success": True,

        "method": "Online Payment",

        "transaction_id": transaction_id

    }