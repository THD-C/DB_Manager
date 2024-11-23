import pytest
import src.Service as Service
import src.DB as DB
import tests.helpers as helpers

import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from order.order_pb2 import OrderDetails


@pytest.fixture(autouse=True)
def setup():
    DB.create_tables(drop_existing=True)
    helpers.register_user(Service.User())
    helpers.create_wallet(Service.Wallet())


def test_create_order_success():
    s = Service.Order()
    dateCreated = Timestamp()
    dateCreated.FromDatetime(datetime.datetime(2021, 1, 1))
    dateExecuted = Timestamp()
    dateExecuted.FromDatetime(datetime.datetime(2021, 1, 1))
    
    o_resp = s.CreateOrder(
        OrderDetails(
            user_id="1",
            date_created=dateCreated,
            date_executed=dateExecuted,
            status=0,
            currency="USD",
            nominal="100.0",
            cash_quantity="123",
            price="0.32",
            type=0,
            side=0,
        ),
        None,
    )

    assert o_resp.id != ""
    assert o_resp.currency == "USD"
    assert o_resp.nominal == "100.0"
    assert o_resp.user_id == "1"
