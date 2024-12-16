from src.Service import Payment
from payment.payment_pb2 import PaymentDetails

PAYMENT_1 = PaymentDetails(
    id="fjeu428de", user_id="1", currency="USD", nominal="100.0", state=1
)
PAYMENT_2 = PaymentDetails(
    id="fjdqwvf46432Sf", user_id="1", currency="KGB", nominal="99.0", state=1
)


def create_payment(s: Payment, payment: PaymentDetails = PAYMENT_1) -> PaymentDetails:
    return s.CreatePayment(
        payment,
        None,
    )
