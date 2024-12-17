from transaction.transaction_pb2_grpc import TransactionServicer
import transaction.transaction_pb2 as gRPC

import src.DB as DB
import src.Utils as Utils


class Transaction(TransactionServicer):
    def CreateTransaction(self, request: gRPC.TransactionDetails, context):
        try:
            with DB.Session() as s:
                transaction = DB.Transaction.create_model(DB.Transaction, request)
                transaction.insert(s)

            return Utils.create_grpc_model(gRPC.TransactionDetails, transaction)
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.TransactionDetails()

    def GetTransaction(self, request: gRPC.TransactionID, context):
        try:
            with DB.Session() as s:
                transaction = s.query(DB.Transaction).filter_by(id=request.id).first()

            return Utils.create_grpc_model(gRPC.TransactionDetails, transaction)
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.TransactionDetails()

    def GetTransactionList(self, request: gRPC.WalletID, context):
        try:
            with DB.Session() as s:
                transactions = (
                    s.query(DB.Transaction)
                    .filter(DB.Transaction.wallet_id == request.id)
                    .all()
                )

            return Utils.create_grpc_list_model(
                gRPC.TransactionList, gRPC.TransactionDetails, transactions
            )
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.TransactionList()

    def DeleteTransaction(self, request: gRPC.TransactionID, context):
        try:
            with DB.Session() as s:
                transaction = s.query(DB.Transaction).filter_by(id=request.id).first()
                if transaction:
                    transaction.delete(s)
            return Utils.create_grpc_model(gRPC.TransactionDetails, transaction)
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.TransactionDetails()

    def UpdateTransaction(self, request: gRPC.TransactionDetails, context):
        try:
            with DB.Session() as s:
                transaction = s.query(DB.Transaction).filter_by(id=request.id).first()
                if transaction:
                    transaction.update(
                        s, DB.Transaction.create_model(DB.Transaction, request)
                    )
            return Utils.create_grpc_model(gRPC.TransactionDetails, transaction)
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.TransactionDetails()
