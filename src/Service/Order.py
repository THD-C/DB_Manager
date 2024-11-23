from order.order_pb2_grpc import OrderServicer
import order.order_pb2 as gRPC

import src.DB as DB
import src.Utils as Utils


class Order(OrderServicer):

    def CreateOrder(self, request: gRPC.OrderDetails, context):
        try:
            with DB.Session() as s:
                order = DB.Order.create_model(DB.Order, request)
                order.insert(s)

            return Utils.create_grpc_model(gRPC.OrderDetails, order)
        except Exception as e:
            print(e)
        return gRPC.OrderDetails()

    def GetOrder(self, request: gRPC.OrderID, context):
        try:
            with DB.Session() as s:
                order = s.query(DB.Order).filter_by(id=request.id).first()

            return Utils.create_grpc_model(gRPC.OrderDetails, order)
        except Exception as e:
            print(e)
        return gRPC.OrderDetails()

    def GetOrderList(self, request: gRPC.UserID, context):
        try:
            with DB.Session() as s:
                orders = s.query(DB.Order).filter(DB.Order.user_id == request.id).all()

            return Utils.create_grpc_list_model(
                gRPC.OrderList, gRPC.OrderDetails, orders
            )
        except Exception as e:
            print(e)
        return gRPC.OrderList()

    def DeleteOrder(self, request: gRPC.OrderID, context):
        try:
            with DB.Session() as s:
                order = s.query(DB.Order).filter_by(id=request.id).first()
                if order:
                    order.delete(s)
            return Utils.create_grpc_model(gRPC.OrderDetails, order)
        except Exception as e:
            print(e)
        return gRPC.OrderDetails()

    def UpdateOrder(self, request: gRPC.OrderDetails, context):
        try:
            with DB.Session() as s:
                order = s.query(DB.Order).filter_by(id=request.id).first()
                if order:
                    order.update(s, DB.Order.create_model(DB.Order, request))
            return Utils.create_grpc_model(gRPC.OrderDetails, order)
        except Exception as e:
            print(e)
        return gRPC.OrderDetails()