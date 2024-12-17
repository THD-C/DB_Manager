from wallet.wallet_pb2_grpc import WalletsServicer
import wallet.wallet_pb2 as grpcWallet

import src.DB as DB
import src.Utils as Utils


class Wallet(WalletsServicer):
    def CreateWallet(self, request: grpcWallet.Wallet, context) -> grpcWallet.Wallet:
        wallet = DB.Wallet.create_model(DB.Wallet, request)
        try:
            with DB.Session() as s:
                existing_wallet = (
                    s.query(DB.Wallet)
                    .filter(
                        DB.Wallet.currency == wallet.currency,
                        DB.Wallet.user_id == wallet.user_id,
                    )
                    .first()
                )
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)

        if existing_wallet:
            return Utils.create_grpc_model(grpcWallet.Wallet, existing_wallet)

        try:
            with DB.Session() as s:
                wallet.insert(s)
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
            return Utils.create_grpc_model(grpcWallet.Wallet, None)
        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def UpdateWallet(self, request: grpcWallet.Wallet, context) -> grpcWallet.Wallet:
        try:
            with DB.Session() as s:
                wallet = (
                    s.query(DB.Wallet).filter(DB.Wallet.id == int(request.id)).first()
                )
                if wallet:
                    wallet.update(s, DB.Wallet.create_model(DB.Wallet, request))

                    wallet_to_check = (
                        s.query(DB.Wallet).filter(DB.Wallet.id == wallet.id).first()
                    )

                    if wallet_to_check == wallet:
                        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)
                    else:
                        wallet.id = None

        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
            return Utils.create_grpc_model(grpcWallet.Wallet, None)

        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def DeleteWallet(self, request: grpcWallet.WalletID, context):
        try:
            with DB.Session() as s:
                wallet = s.query(DB.Wallet).filter(DB.Wallet.id == request.id).first()
                if wallet:
                    wallet.delete(s)
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
            wallet.id = None

        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def GetWallet(self, request: grpcWallet.WalletID, context) -> grpcWallet.Wallet:
        wallet = None
        try:
            with DB.Session() as s:
                wallet = s.query(DB.Wallet).filter(DB.Wallet.id == request.id).first()
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return Utils.create_grpc_model(grpcWallet.Wallet, wallet)

    def GetUsersWallets(
        self, request: grpcWallet.UserID, context
    ) -> grpcWallet.WalletList:
        wallets = []
        try:
            with DB.Session() as s:
                wallets = (
                    s.query(DB.Wallet).filter(DB.Wallet.user_id == request.id).all()
                )
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
            pass
        return Utils.create_grpc_list_model(
            grpcWallet.WalletList, grpcWallet.Wallet, wallets
        )
