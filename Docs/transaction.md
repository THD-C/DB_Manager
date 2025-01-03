# Protocol Documentation

<a name="top"></a>

## Table of Contents

- [operation_type.proto](#operation_type-proto)
  - [OperationType](#transaction-OperationType)
- [transaction.proto](#transaction-proto)

  - [TransactionDetails](#transaction-TransactionDetails)
  - [TransactionID](#transaction-TransactionID)
  - [TransactionList](#transaction-TransactionList)
  - [WalletID](#transaction-WalletID)

  - [Transaction](#transaction-Transaction)

- [Scalar Value Types](#scalar-value-types)

<a name="operation_type-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## operation_type.proto

<a name="transaction-OperationType"></a>

### OperationType

| Name                     | Number | Description                      |
| ------------------------ | ------ | -------------------------------- |
| OPERATION_TYPE_UNDEFINED | 0      | Undefined.                       |
| OPERATION_TYPE_IN        | 1      | Funds added to wallet.           |
| OPERATION_TYPE_OUT       | 2      | Funds withdrawn from wallet.     |
| OPERATION_TYPE_ORDER_IN  | 3      | Funds added from an order.       |
| OPERATION_TYPE_ORDER_OUT | 4      | Funds withdrawn due to an order. |

<a name="transaction-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## transaction.proto

<a name="transaction-TransactionDetails"></a>

### TransactionDetails

Represents a financial transaction affecting a wallet.

| Field          | Type                                                    | Label | Description                                                                                       |
| -------------- | ------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------- |
| id             | [string](#string)                                       |       | Unique string ID for the transaction.                                                             |
| date           | [google.protobuf.Timestamp](#google-protobuf-Timestamp) |       | Date when the transaction occurred.                                                               |
| nominal_value  | [string](#string)                                       |       | Nominal value of the transaction (amount of currency affected), stored as string for flexibility. |
| operation_type | [OperationType](#transaction-OperationType)             |       | Type of transaction operation.                                                                    |
| wallet_id      | [string](#string)                                       |       | Wallet ID                                                                                         |

<a name="transaction-TransactionID"></a>

### TransactionID

| Field | Type              | Label | Description                                    |
| ----- | ----------------- | ----- | ---------------------------------------------- |
| id    | [string](#string) |       | Unique string ID of the transaction to delete. |

<a name="transaction-TransactionList"></a>

### TransactionList

Represents a list of transaction messages.

| Field        | Type                                                  | Label    | Description                                              |
| ------------ | ----------------------------------------------------- | -------- | -------------------------------------------------------- |
| transactions | [TransactionDetails](#transaction-TransactionDetails) | repeated | Repeated field containing multiple transaction messages. |

<a name="transaction-WalletID"></a>

### WalletID

| Field | Type              | Label | Description                               |
| ----- | ----------------- | ----- | ----------------------------------------- |
| id    | [string](#string) |       | Unique string ID of the wallet to delete. |

<a name="transaction-Transaction"></a>

### Transaction

| Method Name        | Request Type                                          | Response Type                                         | Description |
| ------------------ | ----------------------------------------------------- | ----------------------------------------------------- | ----------- |
| CreateTransaction  | [TransactionDetails](#transaction-TransactionDetails) | [TransactionDetails](#transaction-TransactionDetails) |             |
| DeleteTransaction  | [TransactionID](#transaction-TransactionID)           | [TransactionDetails](#transaction-TransactionDetails) |             |
| UpdateTransaction  | [TransactionDetails](#transaction-TransactionDetails) | [TransactionDetails](#transaction-TransactionDetails) |             |
| GetTransaction     | [TransactionID](#transaction-TransactionID)           | [TransactionDetails](#transaction-TransactionDetails) |             |
| GetTransactionList | [WalletID](#transaction-WalletID)                     | [TransactionList](#transaction-TransactionList)       |             |
