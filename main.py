from concurrent import futures
import os
import grpc
from grpc_reflection.v1alpha import reflection
import user.user_pb2_grpc as user_pb2_grpc
import user.user_pb2 as user_pb2
import wallet.wallet_pb2_grpc as wallet_pb2_grpc
import wallet.wallet_pb2 as wallet_pb2
import order.order_pb2_grpc as order_pb2_grpc
import order.order_pb2 as order_pb2

import src.DB as DB
import src.Service as Service


DB.create_tables(drop_existing=os.getenv("DROP_EXISTING_DB", True))


def main() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(Service.User(), server)
    wallet_pb2_grpc.add_WalletsServicer_to_server(Service.Wallet(), server)
    order_pb2_grpc.add_OrderServicer_to_server(Service.Order(), server)

    # Enable reflection
    SERVICE_NAMES = (
        user_pb2.DESCRIPTOR.services_by_name["User"].full_name,
        wallet_pb2.DESCRIPTOR.services_by_name["Wallets"].full_name,
        order_pb2.DESCRIPTOR.services_by_name["Order"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
