from user.user_pb2_grpc import UserServicer
from user.user_pb2 import RegResponse, AuthResponse, AuthUser
from sqlalchemy import or_

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

    def Authenticate(self, request: AuthUser, context):
        with DB.Session() as s:
            db_user = (
                s.query(DB.User)
                .filter(
                    or_(
                        DB.User.email == request.login,
                        DB.User.username == request.login,
                    )
                )
                .first()
            )

        if db_user == request:
            return AuthResponse(
                success=True,
                id=str(db_user.ID),
                username=str(db_user.username),
                email=str(db_user.email),
            )

        return AuthResponse(success=False)
