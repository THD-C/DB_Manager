from src.Service import User
from user.user_pb2 import RegUser, RegResponse

USER_REGISTER_REQUEST = RegUser(
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



def register_user(s: User) -> RegResponse:
    return s.Register(
        USER_REGISTER_REQUEST,
        None,
    )
