from payment.payment_pb2_grpc import PaymentServicer
import payment.payment_pb2 as gRPC
import payment.payment_state_pb2 as payment_state

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
                payment = s.query(DB.Payment).filter_by(id=request.id).first()
                if payment:
                    payment.update(s, request)
                    return Utils.create_grpc_model(gRPC.PaymentDetails, payment)
        except Exception as e:
            print(e)
        return gRPC.PaymentDetails()

    def GetPayments(self, request: gRPC.UserID, context):
        try:
            with DB.Session() as s:
                payments = s.query(DB.Payment).filter_by(user_id=request.user_id).all()

            return Utils.create_grpc_list_model(
                gRPC.PaymentList, gRPC.PaymentDetails, payments
            )
        except Exception as e:
            print(e)
        return gRPC.PaymentList()

    def GetPayment(self, request: gRPC.PaymentID, context):
        try:
            with DB.Session() as s:
                payment = s.query(DB.Payment).filter_by(id=request.id).first()

            return Utils.create_grpc_model(gRPC.PaymentDetails, payment)
        except Exception as e:
            print(e)
        return gRPC.PaymentDetails()

    def GetUnpaidPayments(self, request, context):
        try:
            with DB.Session() as s:
                payments = (
                    s.query(DB.Payment)
                    .filter_by(state=int(payment_state.PAYMENT_STATE_PENDING))
                    .all()
                )

            return Utils.create_grpc_list_model(
                gRPC.PaymentList, gRPC.PaymentDetails, payments
            )
        except Exception as e:
            print(e)
        return gRPC.PaymentList()
