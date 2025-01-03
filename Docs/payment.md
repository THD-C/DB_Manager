# Protocol Documentation

<a name="top"></a>

## Table of Contents

- [payment.proto](#payment-proto)

  - [PaymentDetails](#payment-PaymentDetails)
  - [PaymentID](#payment-PaymentID)
  - [PaymentList](#payment-PaymentList)
  - [UnpaidSessions](#payment-UnpaidSessions)
  - [UserID](#payment-UserID)

  - [Payment](#payment-Payment)

- [payment_state.proto](#payment_state-proto)
  - [PaymentState](#payment-PaymentState)
- [Scalar Value Types](#scalar-value-types)

<a name="payment-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## payment.proto

<a name="payment-PaymentDetails"></a>

### PaymentDetails

Represents made payment

| Field    | Type                                  | Label | Description |
| -------- | ------------------------------------- | ----- | ----------- |
| id       | [string](#string)                     |       |             |
| user_id  | [string](#string)                     |       |             |
| currency | [string](#string)                     |       |             |
| nominal  | [string](#string)                     |       |             |
| state    | [PaymentState](#payment-PaymentState) |       |             |

<a name="payment-PaymentID"></a>

### PaymentID

Filter, which can be used to provide Payment ID

| Field | Type              | Label | Description |
| ----- | ----------------- | ----- | ----------- |
| id    | [string](#string) |       |             |

<a name="payment-PaymentList"></a>

### PaymentList

Represents a list of payments

| Field    | Type                                      | Label    | Description |
| -------- | ----------------------------------------- | -------- | ----------- |
| payments | [PaymentDetails](#payment-PaymentDetails) | repeated |             |

<a name="payment-UnpaidSessions"></a>

### UnpaidSessions

Filter, which can be used to provide unpaid payments

| Field  | Type          | Label | Description |
| ------ | ------------- | ----- | ----------- |
| unpaid | [bool](#bool) |       |             |

<a name="payment-UserID"></a>

### UserID

Filter, which can be used to provide User ID

| Field   | Type              | Label | Description |
| ------- | ----------------- | ----- | ----------- |
| user_id | [string](#string) |       |             |

<a name="payment-Payment"></a>

### Payment

| Method Name       | Request Type                              | Response Type                             | Description                                       |
| ----------------- | ----------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| CreatePayment     | [PaymentDetails](#payment-PaymentDetails) | [PaymentDetails](#payment-PaymentDetails) | Create a new payment.                             |
| UpdatePayment     | [PaymentDetails](#payment-PaymentDetails) | [PaymentDetails](#payment-PaymentDetails) | Updates an existing payment.                      |
| GetPayments       | [UserID](#payment-UserID)                 | [PaymentList](#payment-PaymentList)       | Get all payments associated with provided User ID |
| GetPayment        | [PaymentID](#payment-PaymentID)           | [PaymentDetails](#payment-PaymentDetails) | Get single payment based on Payment ID            |
| GetUnpaidPayments | [UnpaidSessions](#payment-UnpaidSessions) | [PaymentList](#payment-PaymentList)       | Get all unpaid payments                           |

<a name="payment_state-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## payment_state.proto

<a name="payment-PaymentState"></a>

### PaymentState

| Name                    | Number | Description |
| ----------------------- | ------ | ----------- |
| PAYMENT_STATE_UNKNOWN   | 0      |             |
| PAYMENT_STATE_PENDING   | 1      |             |
| PAYMENT_STATE_ACCEPTED  | 2      |             |
| PAYMENT_STATE_CANCELLED | 3      |             |
