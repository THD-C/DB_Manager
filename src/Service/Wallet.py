from wallet.wallet_pb2_grpc import WalletsServicer
import wallet.wallet_pb2 as grpcWallet

import src.DB as DB
import src.Utils as Utils


class Wallet(WalletsServicer):
    def createWallet(self, request: grpcWallet.Wallet, context) -> grpcWallet.Wallet:
        wallet = DB.Wallet.create_model(DB.Wallet, request)
        try:
            with DB.Session() as s:
                wallet.insert(s)
        except Exception as e:
            pass
        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def updateWallet(self, request: grpcWallet.Wallet, context) -> grpcWallet.Wallet:
        try:
            with DB.Session() as s:
                wallet = (
                    s.query(DB.Wallet).filter(DB.Wallet.id == int(request.id)).first()
                )
                wallet.update(s, DB.Wallet.create_model(DB.Wallet, request))

                wallet_to_check = (
                    s.query(DB.Wallet).filter(DB.Wallet.id == wallet.id).first()
                )

            if wallet_to_check == wallet:
                return Utils.create_grpc_model(grpcWallet.Wallet, wallet)
            else:
                wallet.id = None

        except Exception as e:
            pass

        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def deleteWallet(self, request: grpcWallet.WalletID, context):
        try:
            with DB.Session() as s:
                wallet = s.query(DB.Wallet).filter(DB.Wallet.id == request.id).first()
                wallet.delete(s)
        except Exception as e:
            wallet.id = None

        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def getWallet(self, request: grpcWallet.WalletID, context) -> grpcWallet.Wallet:
        wallet = None
        try:
            with DB.Session() as s:
                wallet = s.query(DB.Wallet).filter(DB.Wallet.id == request.id).first()
        except Exception as e:
            pass
        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def getUsersWallets(
        self, request: grpcWallet.UserID, context
    ) -> grpcWallet.WalletList:
        wallets = []
        try:
            with DB.Session() as s:
                wallets = (
                    s.query(DB.Wallet).filter(DB.Wallet.user_id == request.id).all()
                )
        except Exception as e:
            print(e)
            pass
        return Utils.create_grpc_list_model(
            grpcWallet.WalletList, grpcWallet.Wallet, wallets
        )
