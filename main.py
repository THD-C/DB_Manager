from concurrent import futures
import os
import grpc
from grpc_reflection.v1alpha import reflection
import user_pb2_grpc as user_pb2_grpc
import user_pb2 as user_pb2

import src.DB as DB
import src.Service as Service
import src.Utils as Utils


DB.create_tables(drop_existing=os.getenv("DROP_EXISTING_DB", True))

def main() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    user_pb2_grpc.add_UserServicer_to_server(Service.User(), server)
    
    
    # Enable reflection
    SERVICE_NAMES = (
        user_pb2.DESCRIPTOR.services_by_name['User'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    

if __name__ == "__main__":
    main()
