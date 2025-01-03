# DB_Manager

![image](/ERD.png)

This Python-based microservice facilitates communication with a PostgreSQL database, offering a comprehensive set of CRUD operations. Key features include:

- ORM with `SQLModel`: Leverages the SQLModel library for object-relational mapping to interact seamlessly with the database.
- `OpenTelemetry` Integration: Implements distributed tracing using OpenTelemetry, sending trace data to Grafana Tempo (host: `Tempo`,  port: `4317`), an open-source, high-performance tracing backend.
- `Prometheus Metrics`: Exposes Prometheus-compatible metrics on port `8111` for monitoring and observability.
- `RPC Server`: Operates a gRPC server on port `50051` for efficient and reliable communication.

Microservice is optimized for scalability and observability, making it ideal for modern, distributed applications.

# gRPC Services

## User

| Method Name    | Request Type                                         | Response Type                                  | Description                                        |
| -------------- | ---------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- |
| Authenticate   | [AuthUser](/Docs/user.md#authuser)                   | [AuthResponse](/Docs/user.md#authresponse)     | Authenticate user                                  |
| Register       | [RegUser](/Docs/user.md#reguser)                     | [RegResponse](/Docs/user.md#regresponse)       | Register new user                                  |
| GetUserDetails | [ReqGetUserDetails](/Docs/user.md#reqgetuserdetails) | [UserDetails](/Docs/user.mduserdetails)        | Get user details                                   |
| Update         | [ReqUpdateUser](/Docs/user.md#requpdateuser)         | [ResultResponse](/Docs/user.md#resultresponse) | Update user data                                   |
| Delete         | [ReqDeleteUser](/Docs/user.md#reqdeleteuser)         | [ResultResponse](/Docs/user.md#resultresponse) | Delete user                                        |
| ChangePassword | [ChangePass](/Docs/user.md#changepass)               | [ResultResponse](/Docs/user.md#resultresponse) | Change user password                               |
| GetAllUsers    | [AllUsersRequest](/Docs/user.md#allusersrequest)     | [UsersList](/Docs/user.md#userslist)           | Returns all registered users (used only by admins) |

## Wallets

| Method Name     | Request Type                         | Response Type                            | Description                             |
| --------------- | ------------------------------------ | ---------------------------------------- | --------------------------------------- |
| CreateWallet    | [Wallet](/Docs/wallet.md#wallet)     | [Wallet](/Docs/wallet.md#wallet)         | Create a new wallet for a user.         |
| UpdateWallet    | [Wallet](/Docs/wallet.md#wallet)     | [Wallet](/Docs/wallet.md#wallet)         | Update an existing wallet.              |
| DeleteWallet    | [WalletID](/Docs/wallet.md#walletid) | [Wallet](/Docs/wallet.md#wallet)         | Delete a wallet.                        |
| GetWallet       | [WalletID](/Docs/wallet.md#walletid) | [Wallet](/Docs/wallet.md#wallet)         | Get a wallet by its ID.                 |
| GetUsersWallets | [UserID](/Docs/wallet.md#userid)     | [WalletList](/Docs/wallet.md#walletlist) | Get all wallets associated with a user. |
| GetAllWallets   | [Empty](/Docs/wallet.md#empty)       | [WalletList](/Docs/wallet.md#walletlist) | Get all wallets.                        |

## Order

| Method Name  | Request Type                                | Response Type                               | Description                                 |
| ------------ | ------------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| CreateOrder  | [OrderDetails](/Docs/order.md#orderdetails) | [OrderDetails](/Docs/order.md#orderdetails) | Create a new order.                         |
| DeleteOrder  | [OrderID](/Docs/order.md#orderid)           | [OrderDetails](/Docs/order.md#orderdetails) | Delete an existing order.                   |
| GetOrder     | [OrderID](/Docs/order.md#orderid)           | [OrderDetails](/Docs/order.md#orderdetails) | Get single order based on Order ID          |
| GetOrders    | [OrderFilter](/Docs/order.md#orderfilter)   | [OrderList](/Docs/order.md#orderlist)       | Get all orders based on filter              |
| GetOrderList | [UserID](/Docs/order.md#userid)             | [OrderList](/Docs/order.md#orderlist)       | Get all orders based on user ID             |
| UpdateOrder  | [OrderDetails](/Docs/order.md#orderdetails) | [OrderDetails](/Docs/order.md#orderdetails) | Update an existing order based on order ID. |

## Payment

| Method Name       | Request Type                                      | Response Type                                     | Description                                       |
| ----------------- | ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| CreatePayment     | [PaymentDetails](/Docs/payment.md#paymentdetails) | [PaymentDetails](/Docs/payment.md#paymentdetails) | Create a new payment.                             |
| UpdatePayment     | [PaymentDetails](/Docs/payment.md#paymentdetails) | [PaymentDetails](/Docs/payment.md#paymentdetails) | Update an existing payment.                       |
| GetPayments       | [UserID](/Docs/payment.md#userid)                 | [PaymentList](/Docs/payment.md#paymentlist)       | Get all payments associated with provided User ID |
| GetPayment        | [PaymentID](/Docs/payment.md#paymentid)           | [PaymentDetails](/Docs/payment.md#paymentdetails) | Get single payment based on Payment ID            |
| GetUnpaidPayments | [UnpaidSessions](/Docs/payment.md#unpaidsessions) | [PaymentList](/Docs/payment.md#paymentlist)       | Get all unpaid                                    |

## Transaction

| Method Name        | Request Type                                                  | Response Type                                                 | Description                                              |
| ------------------ | ------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------- |
| CreateTransaction  | [TransactionDetails](/Docs/transaction.md#transactiondetails) | [TransactionDetails](/Docs/transaction.md#transactiondetails) | Create a new transaction.                                |
| DeleteTransaction  | [TransactionID](/Docs/transaction.md#Transactionid)           | [TransactionDetails](/Docs/transaction.md#transactiondetails) | Delete an existing transaction                           |
| UpdateTransaction  | [TransactionDetails](/Docs/transaction.md#transactiondetails) | [TransactionDetails](/Docs/transaction.md#transactiondetails) | Update an existing transaction                           |
| GetTransaction     | [TransactionID](/Docs/transaction.md#Transactionid)           | [TransactionDetails](/Docs/transaction.md#transactiondetails) | Get transaction based on transaction ID                  |
| GetTransactionList | [WalletID](/Docs/transaction.md#walletid)                     | [TransactionList](/Docs/transaction.md#transactionlist)       | Get transactions list associated with provided wallet ID |
