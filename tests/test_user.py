import pytest
import src.Service as Service
import src.DB as DB
import tests.helpers as helpers

from user.user_pb2 import (
    RegUser,
    AuthUser,
    ReqGetUserDetails,
    ReqDeleteUser,
    ReqUpdateUser,
    ChangePass,
    AllUsersRequest,
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
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )

    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username


def test_change_user_password_success():
    s = Service.User()
    r_resp = helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    chg_resp = s.ChangePassword(
        ChangePass(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            old_password=helpers.USER_REGISTER_REQUEST_1.password,
            new_password="NewPass",
        ),
        None,
    )

    a_after_chg = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password="NewPass",
        ),
        None,
    )

    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username

    assert chg_resp.success is True
    assert a_after_chg.success is True


def test_change_user_password_fail():
    s = Service.User()
    r_resp = helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    chg_resp = s.ChangePassword(
        ChangePass(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            old_password="failed_password",
            new_password="NewPass",
        ),
        None,
    )

    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username

    assert chg_resp.success is False


def test_register_without_user_details_success():
    s = Service.User()
    r_resp = s.Register(
        RegUser(
            email=helpers.USER_REGISTER_REQUEST_1.email,
            username=helpers.USER_REGISTER_REQUEST_1.username,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )

    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username


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
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )

    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username


def test_login_with_username_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.username,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )

    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username


def test_login_without_email_1_fail():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login="",
            password=helpers.USER_REGISTER_REQUEST_1.password,
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
            login=helpers.USER_REGISTER_REQUEST_1.email,
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
            login=helpers.USER_REGISTER_REQUEST_1.email,
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
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    user_details = s.GetUserDetails(
        ReqGetUserDetails(id=a_resp.id),
        None,
    )
    assert user_details.username == helpers.USER_REGISTER_REQUEST_1.username
    assert user_details.email == helpers.USER_REGISTER_REQUEST_1.email
    assert user_details.name == helpers.USER_REGISTER_REQUEST_1.name
    assert user_details.surname == helpers.USER_REGISTER_REQUEST_1.surname
    assert user_details.street == helpers.USER_REGISTER_REQUEST_1.street
    assert user_details.building == helpers.USER_REGISTER_REQUEST_1.building
    assert user_details.city == helpers.USER_REGISTER_REQUEST_1.city
    assert user_details.postal_code == helpers.USER_REGISTER_REQUEST_1.postal_code
    assert user_details.country == helpers.USER_REGISTER_REQUEST_1.country


def test_get_user_details_for_user_without_user_details_success():
    s = Service.User()
    r_resp = s.Register(
        RegUser(
            email=helpers.USER_REGISTER_REQUEST_1.email,
            username=helpers.USER_REGISTER_REQUEST_1.username,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )

    user_details = s.GetUserDetails(
        ReqGetUserDetails(id=a_resp.id),
        None,
    )
    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username

    assert user_details.username == helpers.USER_REGISTER_REQUEST_1.username
    assert user_details.email == helpers.USER_REGISTER_REQUEST_1.email
    assert user_details.name == ""
    assert user_details.surname == ""
    assert user_details.street == ""
    assert user_details.building == ""
    assert user_details.city == ""
    assert user_details.postal_code == ""
    assert user_details.country == ""


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


def test_update_password_user_fail():
    s = Service.User()
    helpers.register_user(s)
    s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
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
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
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


def test_update_user_details_without_details_created_on_registration():
    s = Service.User()
    r_resp = s.Register(
        RegUser(
            email=helpers.USER_REGISTER_REQUEST_1.email,
            username=helpers.USER_REGISTER_REQUEST_1.username,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
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

    assert r_resp.success is True
    assert a_resp.success is True
    assert a_resp.email == helpers.USER_REGISTER_REQUEST_1.email
    assert a_resp.username == helpers.USER_REGISTER_REQUEST_1.username

    assert u_resp.success is True
    assert u_resp.id == a_resp.id

    assert a_np_resp.success is True
    assert a_np_resp.id == a_resp.id

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
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
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
    assert a_np_resp.username == helpers.USER_REGISTER_REQUEST_1.username

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
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
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
    s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    u_resp = s.ChangePassword(
        ChangePass(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            old_password=helpers.USER_REGISTER_REQUEST_1.password,
            new_password="NewPass",
        ),
        None,
    )
    a_old_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )

    assert u_resp.success is True

    assert a_old_resp.success is False
    assert a_old_resp.id == ""
    assert a_old_resp.email == ""
    assert a_old_resp.username == ""


def test_delete_user_success():
    s = Service.User()
    helpers.register_user(s)
    a_resp = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    d_resp = s.Delete(
        ReqDeleteUser(
            id=a_resp.id,
            mail=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    auth_after_delete = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
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
            login=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    d_resp = s.Delete(
        ReqDeleteUser(
            id="1231341421313",
            mail=helpers.USER_REGISTER_REQUEST_1.email,
            password=helpers.USER_REGISTER_REQUEST_1.password,
        ),
        None,
    )
    assert d_resp.success is False
    assert d_resp.id == ""


def test_get_registered_users_empty_success():
    s = Service.User()
    resp = s.GetAllUsers(AllUsersRequest(), None)

    assert len(resp.user_data) == 0


def test_get_registered_users_3_users_success():
    s = Service.User()
    helpers.register_user(s)
    helpers.register_user(s, helpers.USER_REGISTER_REQUEST_2)
    helpers.register_user(s, helpers.USER_REGISTER_REQUEST_3)

    resp = s.GetAllUsers(AllUsersRequest(), None)

    assert len(resp.user_data) == 3


def test_get_registered_users_users_modified_type_success():
    s = Service.User()
    helpers.register_user(s)
    helpers.register_user(s, helpers.USER_REGISTER_REQUEST_2)
    helpers.register_user(s, helpers.USER_REGISTER_REQUEST_3)

    a_resp_2 = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_2.email,
            password=helpers.USER_REGISTER_REQUEST_2.password,
        ),
        None,
    )

    a_resp_3 = s.Authenticate(
        AuthUser(
            login=helpers.USER_REGISTER_REQUEST_3.email,
            password=helpers.USER_REGISTER_REQUEST_3.password,
        ),
        None,
    )

    _ = s.Update(
        ReqUpdateUser(id=a_resp_2.id, user_type=1),
        None,
    )

    _ = s.Update(
        ReqUpdateUser(id=a_resp_3.id, user_type=2),
        None,
    )

    resp = s.GetAllUsers(AllUsersRequest(), None)

    assert len(resp.user_data) == 3
    assert resp.user_data[0].user_type == 0
    assert resp.user_data[1].user_type == 1
    assert resp.user_data[2].user_type == 2
