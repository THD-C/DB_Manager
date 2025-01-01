import pytest
import src.Service as Service
import tests.helpers as helpers

from wallet.wallet_pb2 import Wallet, WalletID, UserID, Empty
from src.DB.start.create_tables import create_tables


@pytest.fixture(autouse=True)
def setup():
    create_tables(drop_existing=True)
    helpers.register_user(Service.User())


def test_create_wallet_success():
    s = Service.Wallet()
    w_resp = s.CreateWallet(
        helpers.WALLET_1,
        None,
    )

    assert w_resp.id != ""
    assert w_resp.currency == helpers.WALLET_1.currency
    assert w_resp.value == helpers.WALLET_1.value
    assert w_resp.user_id == helpers.WALLET_1.user_id


def test_create_wallet_fail():
    s = Service.Wallet()
    w_resp = s.CreateWallet(
        Wallet(
            currency=helpers.WALLET_1.currency,
            value=helpers.WALLET_1.value,
        ),
        None,
    )

    assert w_resp.id == ""
    assert w_resp.currency == ""
    assert w_resp.value == ""
    assert w_resp.user_id == ""


def test_update_wallet_success():
    s = Service.Wallet()
    helpers.create_wallet(s)
    w_resp = s.UpdateWallet(
        Wallet(
            id="1",
            currency=helpers.WALLET_2.currency,
            value=helpers.WALLET_2.value,
            user_id=helpers.WALLET_1.user_id,
        ),
        None,
    )

    assert w_resp.id == "1"
    assert w_resp.currency == helpers.WALLET_2.currency
    assert w_resp.value == helpers.WALLET_2.value
    assert w_resp.user_id == helpers.WALLET_1.user_id


def test_update_wallet_fail():
    s = Service.Wallet()
    helpers.create_wallet(s)
    w_resp = s.UpdateWallet(
        Wallet(
            currency=helpers.WALLET_2.currency,
            value=helpers.WALLET_2.currency,
            user_id=helpers.WALLET_1.user_id,
        ),
        None,
    )

    assert w_resp.id == ""
    assert w_resp.currency == ""
    assert w_resp.value == ""
    assert w_resp.user_id == ""


def test_delete_wallet_success():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)
    helpers.create_wallet(s, helpers.WALLET_3)

    w_resp = s.DeleteWallet(
        WalletID(
            id="2",
        ),
        None,
    )

    assert w_resp.id == "2"
    assert w_resp.currency == helpers.WALLET_2.currency
    assert w_resp.value == helpers.WALLET_2.value
    assert w_resp.user_id == helpers.WALLET_2.user_id


def test_delete_wallet_fail():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)
    helpers.create_wallet(s, helpers.WALLET_3)

    w_resp = s.DeleteWallet(
        WalletID(
            id="1234567",
        ),
        None,
    )

    assert w_resp.id == ""
    assert w_resp.currency == ""
    assert w_resp.value == ""
    assert w_resp.user_id == ""


def test_get_all_wallets_empty_success():
    s = Service.Wallet()
    w_resp = s.GetAllWallets(
        Empty(),
        None,
    )
    assert len(w_resp.wallets) == 0


def test_get_all_wallets_success():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)
    helpers.create_wallet(s, helpers.WALLET_3)
    w_resp = s.GetAllWallets(
        Empty(),
        None,
    )
    assert len(w_resp.wallets) == 3


def test_get_wallet_2_success():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)
    helpers.create_wallet(s, helpers.WALLET_3)

    w_resp = s.GetWallet(
        WalletID(
            id="2",
        ),
        None,
    )

    assert w_resp.id == "2"
    assert w_resp.currency == helpers.WALLET_2.currency
    assert w_resp.value == helpers.WALLET_2.value
    assert w_resp.user_id == helpers.WALLET_2.user_id


def test_get_wallet_3_success():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)
    helpers.create_wallet(s, helpers.WALLET_3)

    w_resp = s.GetWallet(
        WalletID(
            id="3",
        ),
        None,
    )

    assert w_resp.id == "3"
    assert w_resp.currency == helpers.WALLET_3.currency
    assert w_resp.value == helpers.WALLET_3.value
    assert w_resp.user_id == helpers.WALLET_3.user_id


def test_get_wallet_fail():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)
    helpers.create_wallet(s, helpers.WALLET_3)

    w_resp = s.GetWallet(
        WalletID(
            id="123457898764",
        ),
        None,
    )

    assert w_resp.id == ""
    assert w_resp.currency == ""
    assert w_resp.value == ""
    assert w_resp.user_id == ""


def test_get_user_wallet_list_3_success():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)
    helpers.create_wallet(s, helpers.WALLET_3)

    w_resp = s.GetUsersWallets(
        UserID(
            id="1",
        ),
        None,
    )

    assert len(w_resp.wallets) == 3
    assert [
        helpers.WALLET_1.currency,
        helpers.WALLET_2.currency,
        helpers.WALLET_3.currency,
    ] == [w.currency for w in w_resp.wallets]
    assert [
        helpers.WALLET_1.value,
        helpers.WALLET_2.value,
        helpers.WALLET_3.value,
    ] == [w.value for w in w_resp.wallets]
    assert [
        helpers.WALLET_1.user_id,
        helpers.WALLET_2.user_id,
        helpers.WALLET_3.user_id,
    ] == [w.user_id for w in w_resp.wallets]
    assert [
        "1",
        "2",
        "3",
    ] == [w.id for w in w_resp.wallets]


def test_get_user_wallet_list_2_success():
    s = Service.Wallet()
    helpers.create_wallet(s)
    helpers.create_wallet(s, helpers.WALLET_2)

    w_resp = s.GetUsersWallets(
        UserID(
            id="1",
        ),
        None,
    )

    assert len(w_resp.wallets) == 2
    assert [
        helpers.WALLET_1.currency,
        helpers.WALLET_2.currency,
    ] == [w.currency for w in w_resp.wallets]
    assert [
        helpers.WALLET_1.value,
        helpers.WALLET_2.value,
    ] == [w.value for w in w_resp.wallets]
    assert [
        helpers.WALLET_1.user_id,
        helpers.WALLET_2.user_id,
    ] == [w.user_id for w in w_resp.wallets]
    assert [
        "1",
        "2",
    ] == [w.id for w in w_resp.wallets]


def test_get_user_wallet_list_1_success():
    s = Service.Wallet()
    helpers.create_wallet(s)

    w_resp = s.GetUsersWallets(
        UserID(
            id="1",
        ),
        None,
    )

    assert len(w_resp.wallets) == 1
    assert [
        helpers.WALLET_1.currency,
    ] == [w.currency for w in w_resp.wallets]
    assert [
        helpers.WALLET_1.value,
    ] == [w.value for w in w_resp.wallets]
    assert [
        helpers.WALLET_1.user_id,
    ] == [w.user_id for w in w_resp.wallets]
    assert [
        "1",
    ] == [w.id for w in w_resp.wallets]


def test_get_user_wallet_list_fail():
    s = Service.Wallet()
    helpers.create_wallet(s)

    w_resp = s.GetUsersWallets(
        UserID(
            id="12345678",
        ),
        None,
    )

    assert len(w_resp.wallets) == 0
