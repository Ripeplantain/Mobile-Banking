This project is an attempt to simulate the mobile money banking

Application Features

* Authentication with email verification *
* Send Money *
* Withdraw Money*
* view transfer history*
* view withdraw history*
* My account details *
* Reset Password
* Reset Pin

**Models\**

User Model

* id
* name
* email
* phone number
* password
* balance
* pin
* otp
* is_verified
* created
* updated

Transfer History Model

* id
* amount
* sender -> Foreign Key to User Model
* receiver
* created
* updated

  With Draw History
* id
* amount
* user
* created_at
* updated_at
