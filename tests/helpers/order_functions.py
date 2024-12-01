from order.order_pb2 import OrderDetails
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from src.Service import Order, Wallet
from tests.helpers.wallet_functions import WALLET_1

dateCreated = Timestamp()
dateCreated.FromDatetime(datetime.datetime(2021, 1, 1))
dateExecuted = Timestamp()
dateExecuted.FromDatetime(datetime.datetime(2021, 1, 1))

ORDER_1 = OrderDetails(
    user_id="1",
    wallet_id="1",
    date_created=dateCreated,
    date_executed=dateExecuted,
    status=0,
    currency="USD",
    nominal="100.0",
    cash_quantity="123.0",
    price="0.32",
    type=0,
    side=0,
)
ORDER_2 = OrderDetails(
    user_id="1",
    wallet_id="1",
    date_created=dateCreated,
    date_executed=dateExecuted,
    status=3,
    currency="PLN",
    nominal="98943.0",
    cash_quantity="999.0",
    price="4.89",
    type=3,
    side=2,
)
ORDER_3 = OrderDetails(
    user_id="1",
    wallet_id="1",
    date_created=dateCreated,
    date_executed=dateExecuted,
    status=5,
    currency="EUR",
    nominal="12342.0",
    cash_quantity="1.0",
    price="500.32",
    type=1,
    side=1,
)


def create_order(s: Order, order: OrderDetails = ORDER_1) -> OrderDetails:
    sw = Wallet()
    sw.CreateWallet(
        WALLET_1,
        None,
    )
    return s.CreateOrder(
        order,
        None,
    )
