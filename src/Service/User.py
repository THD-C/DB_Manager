from user.user_pb2_grpc import UserServicer
from user.user_pb2 import (
    RegResponse,
    AuthResponse,
    AuthUser,
    ReqUpdateUser,
    ReqDeleteUser,
    ReqGetUserDetails,
    UserDetails,
    ResultResponse,
)
from sqlalchemy import or_

import src.DB as DB
import src.Utils as Utils


class User(UserServicer):

    def Register(self, request, context):

        user_details = DB.UserDetail.create_model(DB.UserDetail, request)
        user = DB.User.create_model(DB.User, request)
        with DB.Session() as s:
            try:
                user.insert(s)
                if not user_details.check_all_attributes_are_none():
                    user_details.insert(s)
                    user.user_detail_ID = user_details.ID
                    user.update(s, user)
                return RegResponse(success=True)
            except Exception as e:
                print(e)

        return RegResponse(success=False)

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

    def GetUserDetails(self, request: ReqGetUserDetails, context):
        with DB.Session() as s:
            db_user = s.query(DB.User).filter(DB.User.ID == request.id).first()
            if db_user is None:
                return UserDetails()

            db_user_detail = (
                s.query(DB.UserDetail)
                .filter(DB.UserDetail.ID == db_user.user_detail_ID)
                .first()
            )
            
        if db_user_detail is None:
            return UserDetails(
                username=db_user.username,
                email=db_user.email,
            )

        return Utils.create_grpc_model(
            UserDetails,
            {
                **db_user_detail.model_dump(),
                "username": db_user.username,
                "email": db_user.email,
            },
        )

    def Update(self, request: ReqUpdateUser, context):
        error: bool = False

        with DB.Session() as s:
            db_user = s.query(DB.User).filter(DB.User.ID == request.id).first()
            if db_user is None:
                return ResultResponse(success=False)

            if request.email or request.password:
                try:
                    db_user.update(s, DB.User.create_model(DB.User, request))
                except Exception as e:
                    print(e)
                    error = True

            try:
                db_user_detail = (
                    s.query(DB.UserDetail)
                    .filter(DB.UserDetail.ID == db_user.user_detail_ID)
                    .first()
                )
                if db_user_detail is not None:
                    db_user_detail.update(
                        s, DB.UserDetail.create_model(DB.UserDetail, request)
                    )
                else:
                    db_user_detail = DB.UserDetail.create_model(DB.UserDetail, request)
                    db_user_detail.insert(s)
                    db_user.user_detail_ID = db_user_detail.ID
                    db_user.update(s, db_user)
            except Exception as e:
                print(e)
                error = True

        if error:
            return ResultResponse(success=False)

        return ResultResponse(success=True, id=request.id)

    def Delete(self, request: ReqDeleteUser, context):
        try:
            with DB.Session() as s:
                db_user = (
                    s.query(DB.User)
                    .filter(
                        DB.User.ID == int(request.id),
                        DB.User.email == request.mail,
                        DB.User.password == request.password,
                    )
                    .first()
                )
                if db_user is None:
                    return ResultResponse(success=False)

                db_user_detail = (
                    s.query(DB.UserDetail)
                    .filter(DB.UserDetail.ID == db_user.user_detail_ID)
                    .first()
                )

                db_user.delete(s)
                db_user_detail.delete(s)
                return ResultResponse(success=True, id=request.id)
        except Exception as e:
            print(e)

        return ResultResponse(success=False)
