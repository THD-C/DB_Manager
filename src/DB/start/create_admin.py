import grpc
from py_grpc_prometheus.prometheus_client_interceptor import PromClientInterceptor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from secret import secret_pb2_grpc, secret_pb2
from argon2 import PasswordHasher
from src.config import MONGO_MANAGER, MONGO_MANAGER_PORT
from src.Service.User import User
from user.user_pb2 import RegUser, RegResponse, AuthUser, ReqUpdateUser
from user.user_type_pb2 import USER_TYPE_SUPER_ADMIN_USER


def create_admin_user(user_name: str, user_password: str):
    GrpcInstrumentorClient().instrument()
    prometheus_interceptor = PromClientInterceptor()

    mongo_channel = grpc.intercept_channel(
        grpc.insecure_channel(f"{MONGO_MANAGER}:{MONGO_MANAGER_PORT}"),
        prometheus_interceptor,
    )
    secret_stub = secret_pb2_grpc.SecretStoreStub(mongo_channel)
    JWT_SECRET_KEY = secret_stub.GetSecret(
        secret_pb2.SecretName(name="JWT_SECRET_KEY")
    ).value

    password_hash = PasswordHasher().hash(
        user_password, salt=bytes(JWT_SECRET_KEY, "utf-8")
    )
    s = User()

    all_users = s.GetAllUsers(None, None)
    admin = [user for user in all_users.user_data if user.username == user_name]
    if len(admin) > 0:
        print(f"{user_name} user already exists")
        return

    response: RegResponse = s.Register(
        RegUser(
            username=user_name,
            email=f"{user_name}@thdc.pl",
            password=password_hash,
            name="Super",
            surname="Admin",
            street="Zeromskiego",
            building="116",
            city="Lodz",
            postal_code="90-924",
            country="Poland",
        ),
        None,
    )
    if not response.success:
        raise Exception("Failed to create admin user")

    auth = s.Authenticate(AuthUser(login=user_name, password=password_hash), None)

    s.Update(ReqUpdateUser(id=auth.id, user_type=USER_TYPE_SUPER_ADMIN_USER), None)
