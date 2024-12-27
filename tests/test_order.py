import pytest
import src.Service as Service
import src.DB as DB
import tests.helpers as helpers


from order.order_pb2 import OrderID, OrderFilter


@pytest.fixture(autouse=True)
def setup():
    DB.create_tables(drop_existing=True)
    helpers.register_user(Service.User())
    helpers.create_order_wallets()
    helpers.create_wallet(Service.Wallet())


def test_create_order_success():
    s = Service.Order()

    o_resp = s.CreateOrder(
        helpers.ORDER_1,
        None,
    )

    assert o_resp.id != ""
    assert o_resp.nominal == helpers.ORDER_1.nominal
    assert o_resp.user_id == helpers.ORDER_1.user_id
    assert o_resp.cash_quantity == helpers.ORDER_1.cash_quantity
    assert o_resp.price == helpers.ORDER_1.price
    assert o_resp.type == helpers.ORDER_1.type


def test_create_order_fail():
    s = Service.Order()

    o_resp = helpers.create_order(s, None)

    assert o_resp.id == ""
    assert o_resp.nominal == ""
    assert o_resp.user_id == ""
    assert o_resp.cash_quantity == ""
    assert o_resp.price == ""
    assert o_resp.type == 0


def test_get_order_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)

    get_resp = s.GetOrder(
        OrderID(
            id=o_resp.id,
        ),
        None,
    )

    assert get_resp.id == o_resp.id
    assert get_resp.nominal == helpers.ORDER_1.nominal
    assert get_resp.user_id == helpers.ORDER_1.user_id
    assert get_resp.cash_quantity == helpers.ORDER_1.cash_quantity
    assert get_resp.price == helpers.ORDER_1.price
    assert get_resp.type == helpers.ORDER_1.type
    assert get_resp.side == helpers.ORDER_1.side


def test_get_order_fail():
    s = Service.Order()

    get_resp = s.GetOrder(
        OrderID(
            id="1",
        ),
        None,
    )

    assert get_resp.id == ""
    assert get_resp.nominal == ""
    assert get_resp.user_id == ""
    assert get_resp.cash_quantity == ""
    assert get_resp.price == ""
    assert get_resp.type == 0
    assert get_resp.side == 0


def test_get_order_null_id_fail():
    s = Service.Order()

    get_resp = s.GetOrder(
        OrderID(
            id="",
        ),
        None,
    )

    assert get_resp.id == ""
    assert get_resp.nominal == ""
    assert get_resp.user_id == ""
    assert get_resp.cash_quantity == ""
    assert get_resp.price == ""
    assert get_resp.type == 0
    assert get_resp.side == 0


def test_order_list_1_item_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)

    get_resp = s.GetOrderList(
        OrderID(
            id=o_resp.user_id,
        ),
        None,
    )

    assert len(get_resp.orders) == 1
    assert get_resp.orders[0].id == o_resp.id
    assert get_resp.orders[0].nominal == helpers.ORDER_1.nominal
    assert get_resp.orders[0].user_id == helpers.ORDER_1.user_id
    assert get_resp.orders[0].cash_quantity == helpers.ORDER_1.cash_quantity
    assert get_resp.orders[0].price == helpers.ORDER_1.price
    assert get_resp.orders[0].type == helpers.ORDER_1.type
    assert get_resp.orders[0].side == helpers.ORDER_1.side


def test_order_list_3_items_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    get_resp = s.GetOrderList(
        OrderID(
            id=o_resp.user_id,
        ),
        None,
    )
    assert len(get_resp.orders) == 3
    assert [
        helpers.ORDER_1.status,
        helpers.ORDER_2.status,
        helpers.ORDER_3.status,
    ] == [o.status for o in get_resp.orders]
    assert [
        helpers.ORDER_1.nominal,
        helpers.ORDER_2.nominal,
        helpers.ORDER_3.nominal,
    ] == [o.nominal for o in get_resp.orders]
    assert [
        helpers.ORDER_1.cash_quantity,
        helpers.ORDER_2.cash_quantity,
        helpers.ORDER_3.cash_quantity,
    ] == [o.cash_quantity for o in get_resp.orders]
    assert [
        helpers.ORDER_1.price,
        helpers.ORDER_2.price,
        helpers.ORDER_3.price,
    ] == [o.price for o in get_resp.orders]
    assert [
        helpers.ORDER_1.type,
        helpers.ORDER_2.type,
        helpers.ORDER_3.type,
    ] == [o.type for o in get_resp.orders]
    assert [
        helpers.ORDER_1.side,
        helpers.ORDER_2.side,
        helpers.ORDER_3.side,
    ] == [o.side for o in get_resp.orders]
    assert [
        "1",
        "2",
        "3",
    ] == [o.id for o in get_resp.orders]


def test_get_orders_no_filter_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(
            user_id=o_resp.user_id,
        ),
        None,
    )

    assert len(resp.orders) == 3


def test_get_orders_wallet_id_1_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(user_id=o_resp.user_id, wallet_id="2"),
        None,
    )

    assert len(resp.orders) == 1


def test_get_orders_wallet_id_2_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(user_id=o_resp.user_id, wallet_id="1"),
        None,
    )

    assert len(resp.orders) == 3


def test_get_orders_wallet_id_3_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(user_id=o_resp.user_id, wallet_id="4"),
        None,
    )

    assert len(resp.orders) == 1


def test_get_orders_no_user_success():
    s = Service.Order()

    _ = helpers.create_order(s)
    _ = helpers.create_order(s, helpers.ORDER_2)
    _ = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(),
        None,
    )

    assert len(resp.orders) == 3


def test_get_orders_status_1_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(
            user_id=o_resp.user_id,
            status=1,
        ),
        None,
    )

    assert len(resp.orders) == 1


def test_get_orders_status_2_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(
            user_id=o_resp.user_id,
            status=2,
        ),
        None,
    )

    assert len(resp.orders) == 1


def test_get_orders_type_1_failure():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(
            user_id=o_resp.user_id,
            type=1,
        ),
        None,
    )

    assert len(resp.orders) == 1


def test_get_orders_type_2_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(
            user_id=o_resp.user_id,
            type=2,
        ),
        None,
    )

    assert len(resp.orders) == 1


def test_get_orders_side_1_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(
            user_id=o_resp.user_id,
            side=1,
        ),
        None,
    )

    assert len(resp.orders) == 1


def test_get_orders_side_2_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)
    o_resp = helpers.create_order(s, helpers.ORDER_2)
    o_resp = helpers.create_order(s, helpers.ORDER_3)

    resp = s.GetOrders(
        OrderFilter(
            user_id=o_resp.user_id,
            side=2,
        ),
        None,
    )

    assert len(resp.orders) == 1


def test_order_list_0_items_success():
    s = Service.Order()

    get_resp = s.GetOrderList(
        OrderID(
            id="1",
        ),
        None,
    )

    assert len(get_resp.orders) == 0


def test_order_list_Fail():
    s = Service.Order()

    get_resp = s.GetOrderList(
        OrderID(
            id="",
        ),
        None,
    )

    assert len(get_resp.orders) == 0


def test_delete_order_success():
    s = Service.Order()

    o_resp = helpers.create_order(s)

    del_resp = s.DeleteOrder(
        OrderID(
            id=o_resp.id,
        ),
        None,
    )

    assert del_resp.id == o_resp.id
    assert del_resp.nominal == helpers.ORDER_1.nominal
    assert del_resp.user_id == helpers.ORDER_1.user_id
    assert del_resp.cash_quantity == helpers.ORDER_1.cash_quantity
    assert del_resp.price == helpers.ORDER_1.price
    assert del_resp.type == helpers.ORDER_1.type
    assert del_resp.side == helpers.ORDER_1.side


def test_delete_order_fail():
    s = Service.Order()

    del_resp = s.DeleteOrder(
        OrderID(
            id="",
        ),
        None,
    )

    assert del_resp.id == ""
    assert del_resp.nominal == ""
    assert del_resp.user_id == ""
    assert del_resp.cash_quantity == ""
    assert del_resp.price == ""
    assert del_resp.type == 0
    assert del_resp.side == 0


def test_update_order_success():
    s = Service.Order()
    o_resp = helpers.create_order(s)

    o_resp.status = 1

    u_resp = s.UpdateOrder(
        o_resp,
        None,
    )

    g_resp = s.GetOrder(
        OrderID(
            id=o_resp.id,
        ),
        None,
    )

    assert u_resp.id != ""

    assert g_resp.status == 1
    assert g_resp.nominal == helpers.ORDER_1.nominal
    assert g_resp.user_id == helpers.ORDER_1.user_id
    assert g_resp.cash_quantity == helpers.ORDER_1.cash_quantity
    assert g_resp.price == helpers.ORDER_1.price
    assert g_resp.type == helpers.ORDER_1.type
    assert g_resp.side == helpers.ORDER_1.side


def test_update_order_fail():
    s = Service.Order()

    u_resp = s.UpdateOrder(
        helpers.ORDER_1,
        None,
    )
    assert u_resp.id == ""
    assert u_resp.status == 0
    assert u_resp.nominal == ""
    assert u_resp.user_id == ""
    assert u_resp.cash_quantity == ""
    assert u_resp.price == ""
    assert u_resp.type == 0
    assert u_resp.side == 0
