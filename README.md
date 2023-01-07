This project is an attempt to simulate the mobile money banking

Application Features

* Authentication with email verification
* Send Money
* Withdraw Money
* My account details
* Get Loan and Pay Loan
* Reverse Transaction

**Models\**

User Model

* id
* name
* email
* phone number
* password
* otp
* is_verified
* created
* updated

Account Model

* id
* phonenumber
* user -> Foreign Key to User Model
* account_balance
* loan
* pin
* created
* updated

Transaction Model

* id
* amount
* user -> Foreign Key to User Model
* receipient
* account
* type
* created
* updated

Loan Model

* id
* amount
* user -> Foreign Key to User Model
* Account -> Foreign Key to Account Model
* created
* updated
