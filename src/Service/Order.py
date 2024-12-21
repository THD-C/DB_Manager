from order.order_pb2_grpc import OrderServicer
import order.order_pb2 as gRPC
import order.order_status_pb2 as gRPC_OrderStatus
import order.order_side_pb2 as gRPC_OrderSide
import order.order_type_pb2 as gRPC_OrderType

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
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.OrderDetails()

    def GetOrder(self, request: gRPC.OrderID, context):
        try:
            with DB.Session() as s:
                order = s.query(DB.Order).filter_by(id=request.id).first()

            return Utils.create_grpc_model(gRPC.OrderDetails, order)
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.OrderDetails()

    def GetOrders(self, request: gRPC.OrderFilter, context):
        if not request.user_id:
            return gRPC.OrderList()

        try:
            with DB.Session() as s:

                orders_query = s.query(DB.Order).filter(
                    DB.Order.user_id == request.user_id
                )

                if request.wallet_id:
                    orders_query = orders_query.filter(
                        DB.or_(
                            DB.Order.fiat_wallet_id == request.wallet_id,
                            DB.Order.crypto_wallet_id == request.wallet_id,
                        )
                    )

                if not request.status == gRPC_OrderStatus.ORDER_STATUS_UNDEFINED:
                    orders_query = orders_query.filter(
                        DB.Order.status == str(request.status)
                    )

                if not request.type == gRPC_OrderType.ORDER_TYPE_UNDEFINED:
                    orders_query = orders_query.filter(
                        DB.Order.type == str(request.type)
                    )

                if not request.side == gRPC_OrderSide.ORDER_SIDE_UNDEFINED:
                    orders_query = orders_query.filter(
                        DB.Order.side == str(request.side)
                    )

                orders = orders_query.all()

            return Utils.create_grpc_list_model(
                gRPC.OrderList, gRPC.OrderDetails, orders
            )
        except Exception as e:
            Utils.record_trace_exception(e)
            print(e)
        return super().GetOrders(request, context)

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
            Utils.record_trace_exception(e)
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
            Utils.record_trace_exception(e)
            print(e)
        return gRPC.OrderDetails()
