from order.order_pb2 import OrderDetails
from wallet.wallet_pb2 import Wallet as WalletDetails
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from src.Service import Order, Wallet
from tests.helpers.wallet_functions import WALLET_1, WALLET_2, WALLET_3

dateExecuted = Timestamp()
dateExecuted.FromDatetime(datetime.datetime(2021, 1, 1))

ORDER_1 = OrderDetails(
    user_id="1",
    fiat_wallet_id="2",
    crypto_wallet_id="1",
    date_executed=dateExecuted,
    status=1,
    nominal="100.0",
    cash_quantity="123.0",
    price="0.32",
    type=1,
    side=1,
)
ORDER_2 = OrderDetails(
    user_id="1",
    fiat_wallet_id="3",
    crypto_wallet_id="1",
    date_executed=dateExecuted,
    status=2,
    nominal="98943.0",
    cash_quantity="999.0",
    price="4.89",
    type=2,
    side=2,
)
ORDER_3 = OrderDetails(
    user_id="1",
    fiat_wallet_id="4",
    crypto_wallet_id="1",
    date_executed=dateExecuted,
    status=3,
    nominal="12342.0",
    cash_quantity="1.0",
    price="500.32",
    type=3,
    side=3,
)


def create_order(s: Order, order: OrderDetails = ORDER_1) -> OrderDetails:

    return s.CreateOrder(
        order,
        None,
    )


def create_order_wallets() -> None:
    sw = Wallet()
    sw.CreateWallet(
        WalletDetails(
            user_id="1",
            currency="BTC",
            value="1000.0",
            is_crypto=True,
        ),
        None,
    )
    sw.CreateWallet(
        WALLET_1,
        None,
    )
    sw.CreateWallet(
        WALLET_2,
        None,
    )
    sw.CreateWallet(
        WALLET_3,
        None,
    )
