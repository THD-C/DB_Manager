# Protocol Documentation

<a name="top"></a>

## Table of Contents

- [wallet.proto](#wallet-proto)

  - [Empty](#wallet-Empty)
  - [UserID](#wallet-UserID)
  - [Wallet](#wallet-Wallet)
  - [WalletID](#wallet-WalletID)
  - [WalletList](#wallet-WalletList)

  - [Wallets](#wallet-Wallets)

- [Scalar Value Types](#scalar-value-types)

<a name="wallet-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## wallet.proto

<a name="wallet-Empty"></a>

### Empty

Empty message

<a name="wallet-UserID"></a>

### UserID

Filter, which can be used to provide User ID

| Field | Type              | Label | Description |
| ----- | ----------------- | ----- | ----------- |
| id    | [string](#string) |       |             |

<a name="wallet-Wallet"></a>

### Wallet
[w](#wallet)
Represents a user&#39;s wallet containing currency and its balance.

| Field     | Type              | Label | Description                                              |
| --------- | ----------------- | ----- | -------------------------------------------------------- |
| id        | [string](#string) |       | Unique string ID of the wallet.                          |
| currency  | [string](#string) |       | Currency type (e.g., USD, EUR) stored in this wallet.    |
| value     | [string](#string) |       | Current balance of the wallet in the specified currency. |
| user_id   | [string](#string) |       | string ID of the wallet&#39;s owner                      |
| is_crypto | [bool](#bool)     |       | is this wallet a crypto currency wallet                  |

<a name="wallet-WalletID"></a>

### WalletID

Filter, which can be used to provide Wallet ID

| Field | Type              | Label | Description |
| ----- | ----------------- | ----- | ----------- |
| id    | [string](#string) |       |             |

<a name="wallet-WalletList"></a>

### WalletList

Represents a list of Wallet messages.

| Field   | Type                     | Label    | Description                                         |
| ------- | ------------------------ | -------- | --------------------------------------------------- |
| wallets | [Wallet](#wallet-Wallet) | repeated | Repeated field containing multiple Wallet messages. |

<a name="wallet-Wallets"></a>

### Wallets

| Method Name     | Request Type                 | Response Type                    | Description                             |
| --------------- | ---------------------------- | -------------------------------- | --------------------------------------- |
| CreateWallet    | [Wallet](#wallet-Wallet)     | [Wallet](#wallet-Wallet)         | Create a new wallet for a user.         |
| UpdateWallet    | [Wallet](#wallet-Wallet)     | [Wallet](#wallet-Wallet)         | Update an existing wallet.              |
| DeleteWallet    | [WalletID](#wallet-WalletID) | [Wallet](#wallet-Wallet)         | Delete a wallet.                        |
| GetWallet       | [WalletID](#wallet-WalletID) | [Wallet](#wallet-Wallet)         | Get a wallet by its ID.                 |
| GetUsersWallets | [UserID](#wallet-UserID)     | [WalletList](#wallet-WalletList) | Get all wallets associated with a user. |
| GetAllWallets   | [Empty](#wallet-Empty)       | [WalletList](#wallet-WalletList) | Get all wallets.                        |
