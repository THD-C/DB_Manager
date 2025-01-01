from src.Service import User
from user.user_pb2 import RegUser, RegResponse

USER_REGISTER_REQUEST_1 = RegUser(
    username="example_username",
    email="example_email@example.com",
    password="example_password",
    name="Example",
    surname="User",
    street="123 Example St",
    building="Building 1",
    city="Example City",
    postal_code="12345",
    country="Example Country",
)
USER_REGISTER_REQUEST_2 = RegUser(
    username="example_username_2",
    email="example_email@example.com_2",
    password="example_password_2",
    name="Example_2",
    surname="User_2",
    street="123 Example St_2",
    building="Building 1_2",
    city="Example City_2",
    postal_code="12345_2",
    country="Example Country_2",
)
USER_REGISTER_REQUEST_3 = RegUser(
    username="example_username_3",
    email="example_email@example.com_3",
    password="example_password_3",
    name="Example_3",
    surname="User_3",
    street="123 Example St_3",
    building="Building 1_3",
    city="Example City_3",
    postal_code="12345_3",
    country="Example Country_3",
)


def register_user(
    s: User, user_to_register: RegUser = USER_REGISTER_REQUEST_1
) -> RegResponse:
    return s.Register(
        user_to_register,
        None,
    )
