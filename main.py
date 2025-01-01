from concurrent import futures
import os
import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection
import user.user_pb2_grpc as user_pb2_grpc
import user.user_pb2 as user_pb2
import wallet.wallet_pb2_grpc as wallet_pb2_grpc
import wallet.wallet_pb2 as wallet_pb2
import order.order_pb2_grpc as order_pb2_grpc
import order.order_pb2 as order_pb2
import payment.payment_pb2_grpc as payment_pb2_grpc
import payment.payment_pb2 as payment_pb2

from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from py_grpc_prometheus.prometheus_server_interceptor import PromServerInterceptor
from prometheus_client import start_http_server

import src.DB as DB
import src.Service as Service
from src.config import SERVICE_NAME
from src.DB.start.create_tables import create_tables
from src.DB.start.create_admin import create_admin_user

create_tables(drop_existing=os.getenv("DROP_EXISTING_DB", True))
create_admin_user(
    user_name=os.getenv("ADMIN_USER", "admin"),
    user_password=os.getenv("ADMIN_PASS", "admin"),
)


def main() -> None:
    GrpcInstrumentorServer().instrument()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[PromServerInterceptor(enable_handling_time_histogram=True)],
    )

    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set(SERVICE_NAME, health_pb2.HealthCheckResponse.SERVING)

    user_pb2_grpc.add_UserServicer_to_server(Service.User(), server)
    wallet_pb2_grpc.add_WalletsServicer_to_server(Service.Wallet(), server)
    order_pb2_grpc.add_OrderServicer_to_server(Service.Order(), server)
    payment_pb2_grpc.add_PaymentServicer_to_server(Service.Payment(), server)

    # Enable reflection
    SERVICE_NAMES = (
        user_pb2.DESCRIPTOR.services_by_name["User"].full_name,
        wallet_pb2.DESCRIPTOR.services_by_name["Wallets"].full_name,
        order_pb2.DESCRIPTOR.services_by_name["Order"].full_name,
        payment_pb2.DESCRIPTOR.services_by_name["Payment"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    start_http_server(8111)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
