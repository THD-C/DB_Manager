import pytest
import src.Service as Service
import tests.helpers as helpers

from transaction.transaction_pb2 import TransactionDetails, WalletID, TransactionID
from google.protobuf.timestamp_pb2 import Timestamp
from src.DB.start.create_tables import create_tables


@pytest.fixture(autouse=True)
def setup():
    create_tables(drop_existing=True)
    helpers.register_user(Service.User())
    helpers.create_wallet(Service.Wallet())


def test_create_transaction_success():
    s = Service.Transaction()

    t_resp = s.CreateTransaction(
        helpers.TRANSACTION_1,
        None,
    )

    assert t_resp.id != ""
    assert t_resp.date == helpers.TRANSACTION_1.date
    assert t_resp.nominal_value == helpers.TRANSACTION_1.nominal_value
    assert t_resp.operation_type == helpers.TRANSACTION_1.operation_type
    assert t_resp.wallet_id == helpers.TRANSACTION_1.wallet_id


def test_create_transaction_fail():
    s = Service.Transaction()

    t_resp = s.CreateTransaction(
        TransactionDetails(),
        None,
    )

    assert t_resp.id == ""
    assert t_resp.date == Timestamp()
    assert t_resp.nominal_value == ""
    assert t_resp.operation_type == 0
    assert t_resp.wallet_id == ""


def test_get_transaction_success():
    s = Service.Transaction()

    t_resp = helpers.create_transaction(s)

    get_resp = s.GetTransaction(
        TransactionID(
            id=t_resp.id,
        ),
        None,
    )

    assert get_resp.id == t_resp.id
    assert get_resp.date == helpers.TRANSACTION_1.date
    assert get_resp.nominal_value == helpers.TRANSACTION_1.nominal_value
    assert get_resp.operation_type == helpers.TRANSACTION_1.operation_type
    assert get_resp.wallet_id == helpers.TRANSACTION_1.wallet_id


def test_get_transaction_fail():
    s = Service.Transaction()

    get_resp = s.GetTransaction(
        TransactionID(
            id="124242423232432",
        ),
        None,
    )

    assert get_resp.id == ""
    assert get_resp.date == Timestamp()
    assert get_resp.nominal_value == ""
    assert get_resp.operation_type == 0
    assert get_resp.wallet_id == ""


def test_get_transaction_null_id_fail():
    s = Service.Transaction()

    get_resp = s.GetTransaction(
        TransactionID(
            id="",
        ),
        None,
    )

    assert get_resp.id == ""
    assert get_resp.date == Timestamp()
    assert get_resp.nominal_value == ""
    assert get_resp.operation_type == 0
    assert get_resp.wallet_id == ""


def test_order_list_1_item_success():
    s = Service.Transaction()

    t_resp = helpers.create_transaction(s)

    get_resp = s.GetTransactionList(
        WalletID(
            id=t_resp.wallet_id,
        ),
        None,
    )

    assert len(get_resp.transactions) == 1
    assert get_resp.transactions[0].id == t_resp.id
    assert get_resp.transactions[0].date == helpers.TRANSACTION_1.date
    assert get_resp.transactions[0].nominal_value == helpers.TRANSACTION_1.nominal_value
    assert (
        get_resp.transactions[0].operation_type == helpers.TRANSACTION_1.operation_type
    )
    assert get_resp.transactions[0].wallet_id == helpers.TRANSACTION_1.wallet_id


def test_transaction_list_3_items_success():
    s = Service.Transaction()

    helpers.create_transaction(s)
    helpers.create_transaction(s, helpers.TRANSACTION_2)
    helpers.create_transaction(s, helpers.TRANSACTION_3)

    get_resp = s.GetTransactionList(
        WalletID(
            id=helpers.TRANSACTION_1.wallet_id,
        ),
        None,
    )
    assert len(get_resp.transactions) == 3
    assert [
        helpers.TRANSACTION_1.date,
        helpers.TRANSACTION_2.date,
        helpers.TRANSACTION_3.date,
    ] == [t.date for t in get_resp.transactions]
    assert [
        helpers.TRANSACTION_1.nominal_value,
        helpers.TRANSACTION_2.nominal_value,
        helpers.TRANSACTION_3.nominal_value,
    ] == [t.nominal_value for t in get_resp.transactions]
    assert [
        helpers.TRANSACTION_1.operation_type,
        helpers.TRANSACTION_2.operation_type,
        helpers.TRANSACTION_3.operation_type,
    ] == [t.operation_type for t in get_resp.transactions]
    assert [
        helpers.TRANSACTION_1.wallet_id,
        helpers.TRANSACTION_2.wallet_id,
        helpers.TRANSACTION_3.wallet_id,
    ] == [t.wallet_id for t in get_resp.transactions]
    assert [
        "1",
        "2",
        "3",
    ] == [t.id for t in get_resp.transactions]


def test_transaction_list_fail():
    s = Service.Transaction()

    get_resp = s.GetTransactionList(
        WalletID(
            id="",
        ),
        None,
    )

    assert len(get_resp.transactions) == 0


def test_delete_transaction_success():
    s = Service.Transaction()

    t_resp = helpers.create_transaction(s)

    d_resp = s.DeleteTransaction(
        TransactionID(
            id=t_resp.id,
        ),
        None,
    )

    get_resp = s.GetTransaction(
        TransactionID(
            id=t_resp.id,
        ),
        None,
    )

    assert d_resp.id == t_resp.id
    assert d_resp.date == t_resp.date
    assert d_resp.nominal_value == t_resp.nominal_value
    assert d_resp.operation_type == t_resp.operation_type
    assert d_resp.wallet_id == t_resp.wallet_id

    assert get_resp.id == ""
    assert get_resp.date == Timestamp()
    assert get_resp.nominal_value == ""
    assert get_resp.operation_type == 0
    assert get_resp.wallet_id == ""


def test_delete_transaction_fail():
    s = Service.Transaction()

    helpers.create_transaction(s)

    d_resp = s.DeleteTransaction(
        TransactionID(
            id="32123212313",
        ),
        None,
    )

    assert d_resp.id == ""
    assert d_resp.date == Timestamp()
    assert d_resp.nominal_value == ""
    assert d_resp.operation_type == 0
    assert d_resp.wallet_id == ""


def test_delete_transaction_null_id_fail():
    s = Service.Transaction()

    helpers.create_transaction(s)

    d_resp = s.DeleteTransaction(
        TransactionID(
            id="",
        ),
        None,
    )

    assert d_resp.id == ""
    assert d_resp.date == Timestamp()
    assert d_resp.nominal_value == ""
    assert d_resp.operation_type == 0
    assert d_resp.wallet_id == ""


def test_update_transaction_success():
    s = Service.Transaction()

    t_resp = helpers.create_transaction(s)

    t_resp.operation_type = 2

    u_resp = s.UpdateTransaction(
        t_resp,
        None,
    )

    get_resp = s.GetTransaction(
        TransactionID(
            id=t_resp.id,
        ),
        None,
    )

    assert u_resp.id == t_resp.id
    assert u_resp.date == t_resp.date
    assert u_resp.nominal_value == t_resp.nominal_value
    assert u_resp.operation_type == t_resp.operation_type
    assert u_resp.wallet_id == t_resp.wallet_id

    assert get_resp.id == t_resp.id
    assert get_resp.date == t_resp.date
    assert get_resp.nominal_value == t_resp.nominal_value
    assert get_resp.operation_type == t_resp.operation_type
    assert get_resp.wallet_id == t_resp.wallet_id


def test_update_transaction_fail():
    s = Service.Transaction()

    u_resp = s.UpdateTransaction(
        TransactionDetails(),
        None,
    )

    assert u_resp.id == ""
    assert u_resp.date == Timestamp()
    assert u_resp.nominal_value == ""
    assert u_resp.operation_type == 0
    assert u_resp.wallet_id == ""
