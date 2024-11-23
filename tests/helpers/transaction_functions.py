from src.Service import Transaction
from transaction.transaction_pb2 import TransactionDetails
import datetime
from google.protobuf.timestamp_pb2 import Timestamp


dateTest = Timestamp()
dateTest.FromDatetime(datetime.datetime(2021, 1, 1))



TRANSACTION_1 = TransactionDetails(
    date=dateTest,
    nominal_value="100.0",
    operation_type=1,
    wallet_id="1",
)
TRANSACTION_2 = TransactionDetails(
    date=dateTest,
    nominal_value="982.0",
    operation_type=2,
    wallet_id="1",
)
TRANSACTION_3 = TransactionDetails(
    date=dateTest,
    nominal_value="59842.0",
    operation_type=3,
    wallet_id="1",
)

def create_transaction(s: Transaction, transaction: TransactionDetails = TRANSACTION_1) -> TransactionDetails:
    return s.CreateTransaction(
        transaction,
        None,
    )