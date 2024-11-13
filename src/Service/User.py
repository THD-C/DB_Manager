from user_pb2_grpc import UserServicer
from user_pb2 import RegResponse, AuthResponse

import src.DB as DB

class User(UserServicer):
    
    def Register(self, request, context):
        
        user_details = DB.UserDetail.create_model(DB.UserDetail, request)
        user = DB.User.create_model(DB.User, request)
        try:
            with DB.Session() as s:
                user_details.insert(s)
                user.user_detail_ID = user_details.ID
                user.insert(s)
        except:
            return RegResponse(success=False)
        return RegResponse(success=True)
    
    def Authenticate(self, request, context):
        req_user = DB.User.create_model(DB.User, request)
        with DB.Session() as s:
            db_user = s.query(DB.User).filter(DB.User.email == req_user.email).first()
        
        if req_user == db_user:
            return AuthResponse(success=True)
        return AuthResponse(success=False)