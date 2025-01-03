# Protocol Documentation

<a name="top"></a>

## Table of Contents

- [user.proto](#user-proto)

  - [AllUsersRequest](#user-AllUsersRequest)
  - [AuthResponse](#user-AuthResponse)
  - [AuthUser](#user-AuthUser)
  - [ChangePass](#user-ChangePass)
  - [RegResponse](#user-RegResponse)
  - [RegUser](#user-RegUser)
  - [ReqDeleteUser](#user-ReqDeleteUser)
  - [ReqGetUserDetails](#user-ReqGetUserDetails)
  - [ReqUpdateUser](#user-ReqUpdateUser)
  - [ResultResponse](#user-ResultResponse)
  - [UserAdministrativeData](#user-UserAdministrativeData)
  - [UserDetails](#user-UserDetails)
  - [UsersList](#user-UsersList)

  - [User](#user-User)

- [user_detail.proto](#user_detail-proto)
  - [UserDetail](#user-UserDetail)
- [user_type.proto](#user_type-proto)
  - [UserType](#user-UserType)
- [Scalar Value Types](#scalar-value-types)

<a name="user-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## user.proto

<a name="user-AllUsersRequest"></a>

### AllUsersRequest

Empty message to get all users

<a name="user-AuthResponse"></a>

### AuthResponse

Response to indicate the status of the authentication

| Field     | Type                       | Label | Description                   |
| --------- | -------------------------- | ----- | ----------------------------- |
| success   | [bool](#bool)              |       | True if user is authenticated |
| id        | [string](#string)          |       | ID of the user                |
| email     | [string](#string)          |       | Email of the user             |
| username  | [string](#string)          |       | Username of the user          |
| user_type | [UserType](#user-UserType) |       | Type of the user              |

<a name="user-AuthUser"></a>

### AuthUser

Request to authenticate user

| Field    | Type              | Label | Description       |
| -------- | ----------------- | ----- | ----------------- |
| login    | [string](#string) |       | Username or email |
| password | [string](#string) |       | Password          |

<a name="user-ChangePass"></a>

### ChangePass

Request to change user password

| Field        | Type              | Label | Description |
| ------------ | ----------------- | ----- | ----------- |
| login        | [string](#string) |       |             |
| old_password | [string](#string) |       |             |
| new_password | [string](#string) |       |             |

<a name="user-RegResponse"></a>

### RegResponse

Response to indicate the status of the registration

| Field   | Type          | Label | Description                |
| ------- | ------------- | ----- | -------------------------- |
| success | [bool](#bool) |       | True if user is registered |

<a name="user-RegUser"></a>

### RegUser

Request to register new user

| Field       | Type              | Label | Description                          |
| ----------- | ----------------- | ----- | ------------------------------------ |
| username    | [string](#string) |       | Username - can be used to login      |
| email       | [string](#string) |       | Email - can be used to login         |
| password    | [string](#string) |       | Password - used to authenticate user |
| name        | [string](#string) |       | Name of the user                     |
| surname     | [string](#string) |       | Surname of the user                  |
| street      | [string](#string) |       | Street name                          |
| building    | [string](#string) |       | Building number                      |
| city        | [string](#string) |       | City                                 |
| postal_code | [string](#string) |       | Postal code                          |
| country     | [string](#string) |       | Country                              |

<a name="user-ReqDeleteUser"></a>

### ReqDeleteUser

Request to delete user by user ID

| Field | Type              | Label | Description |
| ----- | ----------------- | ----- | ----------- |
| id    | [string](#string) |       |             |

<a name="user-ReqGetUserDetails"></a>

### ReqGetUserDetails

Request to get user details by user ID

| Field | Type              | Label | Description |
| ----- | ----------------- | ----- | ----------- |
| id    | [string](#string) |       |             |

<a name="user-ReqUpdateUser"></a>

### ReqUpdateUser

Request to update user data

| Field       | Type                       | Label | Description |
| ----------- | -------------------------- | ----- | ----------- |
| id          | [string](#string)          |       |             |
| email       | [string](#string)          |       |             |
| password    | [string](#string)          |       |             |
| name        | [string](#string)          |       |             |
| surname     | [string](#string)          |       |             |
| street      | [string](#string)          |       |             |
| building    | [string](#string)          |       |             |
| city        | [string](#string)          |       |             |
| postal_code | [string](#string)          |       |             |
| country     | [string](#string)          |       |             |
| user_type   | [UserType](#user-UserType) |       |             |

<a name="user-ResultResponse"></a>

### ResultResponse

Response to indicate the status and ID of the user which has been updated

| Field   | Type              | Label | Description |
| ------- | ----------------- | ----- | ----------- |
| success | [bool](#bool)     |       |             |
| id      | [string](#string) |       |             |

<a name="user-UserAdministrativeData"></a>

### UserAdministrativeData

Represents user administrative data

| Field     | Type                       | Label | Description |
| --------- | -------------------------- | ----- | ----------- |
| ID        | [string](#string)          |       |             |
| email     | [string](#string)          |       |             |
| username  | [string](#string)          |       |             |
| user_type | [UserType](#user-UserType) |       |             |

<a name="user-UserDetails"></a>

### UserDetails

Represents user details

| Field       | Type                       | Label | Description |
| ----------- | -------------------------- | ----- | ----------- |
| username    | [string](#string)          |       |             |
| email       | [string](#string)          |       |             |
| name        | [string](#string)          |       |             |
| surname     | [string](#string)          |       |             |
| street      | [string](#string)          |       |             |
| building    | [string](#string)          |       |             |
| city        | [string](#string)          |       |             |
| postal_code | [string](#string)          |       |             |
| country     | [string](#string)          |       |             |
| user_type   | [UserType](#user-UserType) |       |             |

<a name="user-UsersList"></a>

### UsersList

Represents a list of users

| Field     | Type                                                   | Label    | Description |
| --------- | ------------------------------------------------------ | -------- | ----------- |
| user_data | [UserAdministrativeData](#user-UserAdministrativeData) | repeated |             |

<a name="user-User"></a>

### User

| Method Name    | Request Type                                 | Response Type                          | Description                                        |
| -------------- | -------------------------------------------- | -------------------------------------- | -------------------------------------------------- |
| Authenticate   | [AuthUser](#user-AuthUser)                   | [AuthResponse](#user-AuthResponse)     | Authenticate user                                  |
| Register       | [RegUser](#user-RegUser)                     | [RegResponse](#user-RegResponse)       | Register new user                                  |
| GetUserDetails | [ReqGetUserDetails](#user-ReqGetUserDetails) | [UserDetails](#user-UserDetails)       | Get user details                                   |
| Update         | [ReqUpdateUser](#user-ReqUpdateUser)         | [ResultResponse](#user-ResultResponse) | Update user data                                   |
| Delete         | [ReqDeleteUser](#user-ReqDeleteUser)         | [ResultResponse](#user-ResultResponse) | Delete user                                        |
| ChangePassword | [ChangePass](#user-ChangePass)               | [ResultResponse](#user-ResultResponse) | Change user password                               |
| GetAllUsers    | [AllUsersRequest](#user-AllUsersRequest)     | [UsersList](#user-UsersList)           | Returns all registered users (used only by admins) |

<a name="user_detail-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## user_detail.proto

<a name="user-UserDetail"></a>

### UserDetail

Detailed information about the user, typically used for profile or identity verification.

| Field       | Type              | Label | Description                                                                |
| ----------- | ----------------- | ----- | -------------------------------------------------------------------------- |
| id          | [string](#string) |       | Unique string ID for user details. Can be opaque and encoded if necessary. |
| name        | [string](#string) |       | User&#39;s first name.                                                     |
| surname     | [string](#string) |       | User&#39;s last name (surname).                                            |
| city        | [string](#string) |       | City where the user resides.                                               |
| postal_code | [string](#string) |       | Postal code for the user&#39;s address.                                    |
| street      | [string](#string) |       | Street name where the user lives.                                          |
| building    | [string](#string) |       | Building number of the user&#39;s residence.                               |

<a name="user_type-proto"></a>

<p align="right"><a href="#top">Top</a></p>

## user_type.proto

<a name="user-UserType"></a>

### UserType

| Name                       | Number | Description                                           |
| -------------------------- | ------ | ----------------------------------------------------- |
| USER_TYPE_NO_ACTION        | 0      | Default value, which indicates no action on user type |
| USER_TYPE_STANDARD_USER    | 1      | Can only display Blog                                 |
| USER_TYPE_BLOGGER_USER     | 2      | Can edit and create Blog                              |
| USER_TYPE_SUPER_ADMIN_USER | 3      | Can do same as Blogger and also manage users          |
