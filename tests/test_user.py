import pytest
import src.Service as Service
import src.DB as DB
import tests.helpers as helpers

from user.user_pb2 import (
    AuthUser,
    ReqGetUserDetails,
)

@pytest.fixture(autouse=True)
def setup():
    DB.create_tables(drop_existing=True)
    print("Setup completed")


def test_register_success():
    s = Service.User()
    r_resp = helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert r_resp.success == True
    assert a_resp.success == True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST.username


def test_register_fail():
    s = Service.User()
    r_resp = helpers.register_user(s)
    r_resp2 = helpers.register_user(s)

    assert r_resp.success == True
    assert r_resp2.success == False


def test_login_with_email_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert a_resp.success == True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST.username


def test_login_with_username_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.username,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert a_resp.success == True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST.username


def test_login_without_email_fail_1():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login="",
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert a_resp.success == False


def test_login_without_email_fail_2():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login="",
            password="",
        ),
        None,
    )

    assert a_resp.success == False


def test_login_without_password_fail():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password="",
        ),
        None,
    )

    assert a_resp.success == False


def test_login_with_wrong_password_fail():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password="wrong_password",
        ),
        None,
    )
    assert a_resp.success == False


def test_get_user_details_success():
    s = Service.User()
    r_resp = helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    user_details = s.GetUserDetails(
        ReqGetUserDetails(id=a_resp.id),
        None,
    )
    assert user_details.username == helpers.USER_REGISTER_REQUEST.username
    assert user_details.email == helpers.USER_REGISTER_REQUEST.email
    assert user_details.name == helpers.USER_REGISTER_REQUEST.name
    assert user_details.surname == helpers.USER_REGISTER_REQUEST.surname
    assert user_details.street == helpers.USER_REGISTER_REQUEST.street
    assert user_details.building == helpers.USER_REGISTER_REQUEST.building
    assert user_details.city == helpers.USER_REGISTER_REQUEST.city
    assert user_details.postal_code == helpers.USER_REGISTER_REQUEST.postal_code
    assert user_details.country == helpers.USER_REGISTER_REQUEST.country


def test_get_user_details_id_does_not_exist_fail():
    s = Service.User()
    r_resp = helpers.register_user(s)
    user_details = s.GetUserDetails(
        ReqGetUserDetails(id="1111"),
        None,
    )
    assert user_details.username == ""
    assert user_details.email == ""
    assert user_details.name == ""
    assert user_details.surname == ""
    assert user_details.street == ""
    assert user_details.building == ""
    assert user_details.city == ""
    assert user_details.postal_code == ""
    assert user_details.country == ""
