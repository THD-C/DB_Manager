from wallet.wallet_pb2_grpc import WalletsServicer
import wallet.wallet_pb2 as grpcWallet

import src.DB as DB
import src.Utils as Utils


class Wallet(WalletsServicer):
    def createWallet(self, request, context):
        wallet = DB.Wallet.create_model(DB.Wallet, request)
        try:
            with DB.Session() as s:
                wallet.insert(s)
        except Exception as e:
            pass
        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)
