This project is an attempt to simulate the mobile money banking

Application Features

* Authentication with sms verification
* Send Money
* Withdraw Money
* My account details
* Get Loan and Pay Loan
* Reverse Transaction


**Models\**

User Model

* id (uuid)
* name
* email
* phone number
* password
* pin
* created
* updated


Account Model

* id
* user -> Foreign Key to User Model
* account_balance
* created
* updated

Transaction Model

* id
* amount
* user -> Foreign Key to User Model
* created
* updated

Loan Model

* id
* amount
* user -> Foreign Key to User Model
* Account -> Foreign Key to Account Model
* created
* updated
