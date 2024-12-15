from src.Service import Payment
from payment.payment_pb2 import PaymentDetails

PAYMENT_1 = PaymentDetails(user_id="1", currency="USD", nominal="100.0", state=1)


def create_payment(s: Payment, payment: PaymentDetails = PAYMENT_1) -> PaymentDetails:
    return s.CreatePayment(
        payment,
        None,
    )
