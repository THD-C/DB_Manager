# Protocol Documentation

<a name="top"></a>

## Table of Contents

- [order.proto](#order-proto)

  - [OrderDetails](#order-OrderDetails)
  - [OrderFilter](#order-OrderFilter)
  - [OrderID](#order-OrderID)
  - [OrderList](#order-OrderList)
  - [UserID](#order-UserID)

  - [Order](#order-Order)

- [order_side.proto](#order_side-proto)
  - [OrderSide](#order-OrderSide)
- [order_status.proto](#order_status-proto)
  - [OrderStatus](#order-OrderStatus)
- [order_type.proto](#order_type-proto)
  - [OrderType](#order-OrderType)
- [Scalar Value Types](#scalar-value-types)

<a name="order-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## order.proto

<a name="order-OrderDetails"></a>

### OrderDetails

Represents a currency order placed by the user, such as buying or selling currency.

| Field            | Type                                                    | Label | Description                                                        |
| ---------------- | ------------------------------------------------------- | ----- | ------------------------------------------------------------------ |
| id               | [string](#string)                                       |       | Unique string ID of the order.                                     |
| user_id          | [string](#string)                                       |       | Foreign key referencing the User who placed the order.             |
| date_created     | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |       | Date when the order was created.                                   |
| date_executed    | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |       | Date when the order was executed.                                  |
| status           | [OrderStatus](#order-OrderStatus)                       |       | Current status of the order.                                       |
| nominal          | [string](#string)                                       |       | Amount of currency involved in the order.                          |
| cash_quantity    | [string](#string)                                       |       | Amount of cash involved in the order, can be NULL if irrelevant.   |
| price            | [string](#string)                                       |       | Price per unit of currency, represented as a string for precision. |
| type             | [OrderType](#order-OrderType)                           |       | Type of the order (e.g., stop loss, take profit).                  |
| side             | [OrderSide](#order-OrderSide)                           |       | Side of the order.                                                 |
| crypto_wallet_id | [string](#string)                                       |       | Wallet_id of crypto wallet                                         |
| fiat_wallet_id   | [string](#string)                                       |       | Wallet_id of Fiat currency wallet                                  |

<a name="order-OrderFilter"></a>

### OrderFilter

Filters which can be applied to the list of orders.

| Field     | Type                              | Label | Description                        |
| --------- | --------------------------------- | ----- | ---------------------------------- |
| user_id   | [string](#string)                 |       | Owner&#39;s user_id.               |
| wallet_id | [string](#string)                 |       | Wallet_id of crypto or Fiat wallet |
| status    | [OrderStatus](#order-OrderStatus) |       | Status of the order to filter by.  |
| type      | [OrderType](#order-OrderType)     |       | Type of the order to filter by.    |
| side      | [OrderSide](#order-OrderSide)     |       | Side of the order to filter by.    |

<a name="order-OrderID"></a>

### OrderID

| Field | Type              | Label | Description                              |
| ----- | ----------------- | ----- | ---------------------------------------- |
| id    | [string](#string) |       | Unique string ID of the order to delete. |

<a name="order-OrderList"></a>

### OrderList

Represents a list of order messages.

| Field  | Type                                | Label    | Description                                        |
| ------ | ----------------------------------- | -------- | -------------------------------------------------- |
| orders | [OrderDetails](#order-OrderDetails) | repeated | Repeated field containing multiple Order messages. |

<a name="order-UserID"></a>

### UserID

| Field | Type              | Label | Description                              |
| ----- | ----------------- | ----- | ---------------------------------------- |
| id    | [string](#string) |       | Unique string ID of the order to delete. |

<a name="order-Order"></a>

### Order

| Method Name  | Request Type                        | Response Type                       | Description                                 |
| ------------ | ----------------------------------- | ----------------------------------- | ------------------------------------------- |
| CreateOrder  | [OrderDetails](#order-OrderDetails) | [OrderDetails](#order-OrderDetails) | Create a new order.                         |
| DeleteOrder  | [OrderID](#order-OrderID)           | [OrderDetails](#order-OrderDetails) | Delete an existing order.                   |
| GetOrder     | [OrderID](#order-OrderID)           | [OrderDetails](#order-OrderDetails) | Get single order based on Order ID          |
| GetOrders    | [OrderFilter](#order-OrderFilter)   | [OrderList](#order-OrderList)       | Get all orders based on filter              |
| GetOrderList | [UserID](#order-UserID)             | [OrderList](#order-OrderList)       | Get all orders based on user ID             |
| UpdateOrder  | [OrderDetails](#order-OrderDetails) | [OrderDetails](#order-OrderDetails) | Update an existing order based on order ID. |

<a name="order_side-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## order_side.proto

<a name="order-OrderSide"></a>

### OrderSide

| Name                 | Number | Description |
| -------------------- | ------ | ----------- |
| ORDER_SIDE_UNDEFINED | 0      |             |
| ORDER_SIDE_BUY       | 1      |             |
| ORDER_SIDE_SELL      | 2      |             |

<a name="order_status-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## order_status.proto

<a name="order-OrderStatus"></a>

### OrderStatus

| Name                             | Number | Description |
| -------------------------------- | ------ | ----------- |
| ORDER_STATUS_UNDEFINED           | 0      |             |
| ORDER_STATUS_ACCEPTED            | 1      |             |
| ORDER_STATUS_REJECTED            | 2      |             |
| ORDER_STATUS_PENDING             | 3      |             |
| ORDER_STATUS_PARTIALLY_COMPLETED | 5      |             |
| ORDER_STATUS_COMPLETED           | 4      |             |
| ORDER_STATUS_CANCELLED           | 6      |             |
| ORDER_STATUS_EXPIRED             | 7      |             |
| ORDER_STATUS_IN_PROGRESS         | 8      |             |

<a name="order_type-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## order_type.proto

<a name="order-OrderType"></a>

### OrderType

| Name                   | Number | Description                                               |
| ---------------------- | ------ | --------------------------------------------------------- |
| ORDER_TYPE_UNDEFINED   | 0      | Undefined state                                           |
| ORDER_TYPE_STOP_LOSS   | 1      | Sell when a certain price below current price is reached. |
| ORDER_TYPE_TAKE_PROFIT | 2      | Sell when a certain price above current price is reached. |
| ORDER_TYPE_INSTANT     | 3      | Immediate execution.                                      |
| ORDER_TYPE_PENDING     | 4      | Pending buy order only.                                   |
