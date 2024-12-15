from payment.payment_pb2_grpc import PaymentServicer
import payment.payment_pb2 as gRPC


import src.DB as DB
import src.Utils as Utils


class Payment(PaymentServicer):
    def CreatePayment(self, request: gRPC.PaymentDetails, context):
        try:
            with DB.Session() as s:
                payment = DB.Payment.create_model(DB.Payment, request)
                payment.insert(s)

            return Utils.create_grpc_model(gRPC.PaymentDetails, payment)
        except Exception as e:
            print(e)
        return gRPC.PaymentDetails()

    def UpdatePayment(self, request: gRPC.PaymentDetails, context):
        try:
            with DB.Session() as s:
                payment = s.query(DB.Payment).filter_by(id=request.user_id).first()
                if payment:
                    payment.update(s, request)
                    return Utils.create_grpc_model(gRPC.PaymentDetails, payment)
        except Exception as e:
            print(e)
        return gRPC.PaymentDetails()

    def GetPayment(self, request: gRPC.UserID, context):
        try:
            with DB.Session() as s:
                payments = s.query(DB.Payment).filter_by(user_id=request.user_id).all()

            return Utils.create_grpc_list_model(
                gRPC.PaymentList, gRPC.PaymentDetails, payments
            )
        except Exception as e:
            print(e)
        return gRPC.PaymentList()
