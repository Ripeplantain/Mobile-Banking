This project is an attempt to simulate the mobile money banking

Application Features

* Authentication with email verification *
* Send Money
* Withdraw Money
* My account details *
* Get Loan and Pay Loan
* Reverse Transaction
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

Loan History

* id
* amount
* user -> Foreign Key to User Model
* Account -> Foreign Key to Account Model
* created
* updated
