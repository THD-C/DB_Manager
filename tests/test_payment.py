import pytest
import src.Service as Service
import src.DB as DB
import tests.helpers as helpers

from payment.payment_pb2 import PaymentDetails, PaymentList, UserID


@pytest.fixture(autouse=True)
def setup():
    DB.create_tables(drop_existing=True)
    helpers.register_user(Service.User())


def test_create_payment_success():
    s = Service.Payment()

    p_resp = s.CreatePayment(
        helpers.PAYMENT_1,
        None,
    )

    assert p_resp.id != ""
    assert p_resp.user_id == helpers.PAYMENT_1.user_id
    assert p_resp.currency == helpers.PAYMENT_1.currency
    assert p_resp.nominal == helpers.PAYMENT_1.nominal
    assert p_resp.state == helpers.PAYMENT_1.state


def test_create_payment_failure():
    s = Service.Payment()
    payment = helpers.PAYMENT_1
    payment.user_id = "1234312"
    p_resp = s.CreatePayment(
        payment,
        None,
    )

    assert p_resp.id == ""
    assert p_resp.user_id == ""
    assert p_resp.currency == ""
    assert p_resp.nominal == ""
    assert p_resp.state == 0


def test_update_payment_success():
    s = Service.Payment()

    p_resp = s.CreatePayment(
        helpers.PAYMENT_1,
        None,
    )

    p_resp.nominal = "200.0"
    p_resp.state = 2

    updated_resp = s.UpdatePayment(
        p_resp,
        None,
    )

    assert updated_resp.id == p_resp.id
    assert updated_resp.user_id == p_resp.user_id
    assert updated_resp.currency == p_resp.currency
    assert updated_resp.nominal == p_resp.nominal
    assert updated_resp.state == p_resp.state


def test_update_payment_failure():
    s = Service.Payment()

    p_resp = s.CreatePayment(
        helpers.PAYMENT_1,
        None,
    )

    p_resp.user_id = "1234312"

    updated_resp = s.UpdatePayment(
        PaymentDetails(),
        None,
    )

    assert updated_resp.id == ""
    assert updated_resp.user_id == ""
    assert updated_resp.currency == ""
    assert updated_resp.nominal == ""
    assert updated_resp.state == 0


def test_get_payment_1_success():
    s = Service.Payment()

    p_resp = s.CreatePayment(
        helpers.PAYMENT_1,
        None,
    )

    get_resp = s.GetPayment(
        UserID(
            user_id=p_resp.user_id,
        ),
        None,
    )

    assert len(get_resp.payments) == 1
    assert get_resp.payments[0].id == p_resp.id
    assert get_resp.payments[0].user_id == p_resp.user_id
    assert get_resp.payments[0].currency == p_resp.currency
    assert get_resp.payments[0].nominal == p_resp.nominal
    assert get_resp.payments[0].state == p_resp.state


def test_get_payment_2_success():
    s = Service.Payment()

    p1_resp = s.CreatePayment(
        helpers.PAYMENT_1,
        None,
    )

    payment = helpers.PAYMENT_1
    payment.currency = "EUR"
    payment.nominal = "200.0"

    p2_resp = s.CreatePayment(
        payment,
        None,
    )

    get_resp = s.GetPayment(
        UserID(
            user_id=p2_resp.user_id,
        ),
        None,
    )

    assert len(get_resp.payments) == 2
    assert get_resp.payments[0].id == p1_resp.id
    assert get_resp.payments[0].user_id == p1_resp.user_id
    assert get_resp.payments[0].currency == p1_resp.currency
    assert get_resp.payments[0].nominal == p1_resp.nominal
    assert get_resp.payments[0].state == p1_resp.state
    assert get_resp.payments[1].id == p2_resp.id
    assert get_resp.payments[1].user_id == p2_resp.user_id
    assert get_resp.payments[1].currency == p2_resp.currency
    assert get_resp.payments[1].nominal == p2_resp.nominal
    assert get_resp.payments[1].state == p2_resp.state


def test_get_payment_failure():
    s = Service.Payment()

    _ = s.CreatePayment(
        helpers.PAYMENT_1,
        None,
    )

    get_resp = s.GetPayment(
        UserID(
            user_id="1234312",
        ),
        None,
    )

    assert len(get_resp.payments) == 0
