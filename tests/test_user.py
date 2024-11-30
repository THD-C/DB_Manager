import pytest
import src.Service as Service
import src.DB as DB
import tests.helpers as helpers

from user.user_pb2 import RegUser, AuthUser, ReqGetUserDetails, ReqDeleteUser, ReqUpdateUser


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

    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST.username

def test_register_without_user_details_success():
    s = Service.User()
    r_resp = s.Register(
        RegUser(
            email=helpers.USER_REGISTER_REQUEST.email,
            username=helpers.USER_REGISTER_REQUEST.username,
            password=helpers.USER_REGISTER_REQUEST.password,
            ),
        None,
    )
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST.username

def test_register_fail():
    s = Service.User()
    r_resp = helpers.register_user(s)
    r_resp2 = helpers.register_user(s)

    assert r_resp.success is True
    assert r_resp2.success is False


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

    assert a_resp.success is True
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

    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST.username


def test_login_without_email_1_fail():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login="",
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert a_resp.success is False


def test_login_without_email_2_fail():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login="",
            password="",
        ),
        None,
    )

    assert a_resp.success is False


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

    assert a_resp.success is False


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
    assert a_resp.success is False


def test_get_user_details_success():
    s = Service.User()
    helpers.register_user(s)
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
    helpers.register_user(s)
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


def test_update_password_user_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    u_resp = s.Update(
        ReqUpdateUser(
            id=a_resp.id,
            password="NewPass",
        ),
        None,
    )

    a_np_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password="NewPass",
        ),
        None,
    )

    assert a_resp.success is True

    assert u_resp.success is True
    assert u_resp.id == a_resp.id

    assert a_np_resp.success is True
    assert a_np_resp.id == a_resp.id
    assert a_np_resp.email == helpers.USER_REGISTER_REQUEST.email
    assert a_np_resp.username == helpers.USER_REGISTER_REQUEST.username


def test_update_password_user_fail():
    s = Service.User()
    helpers.register_user(s)
    s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    u_resp = s.Update(
        ReqUpdateUser(
            id="12213312",
            password="NewPass",
        ),
        None,
    )

    assert u_resp.success is False
    assert u_resp.id == ""


def test_update_user_details_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    u_resp = s.Update(
        ReqUpdateUser(
            id=a_resp.id,
            surname="NewSurname",
            name="NewName",
            street="NewStreet",
            building="NewBuilding",
            city="NewCity",
            country="NewCountry",
            postal_code="NewPostalCode",
        ),
        None,
    )

    user_details = s.GetUserDetails(ReqGetUserDetails(id=a_resp.id), None)

    assert a_resp.success is True

    assert u_resp.success is True
    assert u_resp.id == a_resp.id

    assert user_details.surname == "NewSurname"
    assert user_details.name == "NewName"
    assert user_details.street == "NewStreet"
    assert user_details.building == "NewBuilding"
    assert user_details.city == "NewCity"
    assert user_details.country == "NewCountry"
    assert user_details.postal_code == "NewPostalCode"


def test_update_user_details_and_password_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    u_resp = s.Update(
        ReqUpdateUser(
            id=a_resp.id,
            password="NewPass",
            email="NewUsername@example.com",
            surname="NewSurname",
            name="NewName",
            street="NewStreet",
            building="NewBuilding",
            city="NewCity",
            country="NewCountry",
            postal_code="NewPostalCode",
        ),
        None,
    )

    a_np_resp = s.Authenticate(
        AuthUser(
            login="NewUsername@example.com",
            password="NewPass",
        ),
        None,
    )

    user_details = s.GetUserDetails(ReqGetUserDetails(id=a_resp.id), None)

    assert u_resp.success is True
    assert u_resp.id == a_resp.id

    assert a_np_resp.success is True
    assert a_np_resp.id == a_resp.id
    assert a_np_resp.email == "NewUsername@example.com"
    assert a_np_resp.username == helpers.USER_REGISTER_REQUEST.username

    assert user_details.surname == "NewSurname"
    assert user_details.name == "NewName"
    assert user_details.street == "NewStreet"
    assert user_details.building == "NewBuilding"
    assert user_details.city == "NewCity"
    assert user_details.country == "NewCountry"
    assert user_details.postal_code == "NewPostalCode"


def test_update_user_failure():
    s = Service.User()
    helpers.register_user(s)
    s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    u_resp = s.Update(
        ReqUpdateUser(
            id="12313242",
            password="NewPass",
        ),
        None,
    )

    assert u_resp.success is False
    assert u_resp.id == ""


def test_login_with_old_password_fail():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    u_resp = s.Update(
        ReqUpdateUser(
            id=a_resp.id,
            password="NewPass",
        ),
        None,
    )
    a_old_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert u_resp.success is True
    assert u_resp.id == a_resp.id

    assert a_old_resp.success is False
    assert a_old_resp.id == ""
    assert a_old_resp.email == ""
    assert a_old_resp.username == ""


def test_delete_user_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    d_resp = s.Delete(
        ReqDeleteUser(
            id=a_resp.id,
            mail=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    auth_after_delete = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )

    assert d_resp.success is True
    assert d_resp.id == a_resp.id

    assert auth_after_delete.success is False
    assert auth_after_delete.id == ""
    assert auth_after_delete.email == ""
    assert auth_after_delete.username == ""


def test_delete_user_fail():
    s = Service.User()
    helpers.register_user(s)
    s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    d_resp = s.Delete(
        ReqDeleteUser(
            id="1231341421313",
            mail=helpers.USER_REGISTER_REQUEST.email,
            password=helpers.USER_REGISTER_REQUEST.password,
        ),
        None,
    )
    assert d_resp.success is False
    assert d_resp.id == ""
