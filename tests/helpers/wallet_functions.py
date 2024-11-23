from src.Service import Wallet
from wallet.wallet_pb2 import Wallet as Wallet_pb

WALLET_1 = Wallet_pb(
    value="1000.0",
    currency="USD",
    user_id="1"
)
WALLET_2 = Wallet_pb(
    value="99.0",
    currency="PLN",
    user_id="1"
)
WALLET_3 = Wallet_pb(
    value="89.0",
    currency="EUR",
    user_id="1"
)

def create_wallet(s: Wallet, wallet: Wallet_pb = WALLET_1) -> Wallet_pb:
    return s.createWallet(
        wallet,
        None,
    )