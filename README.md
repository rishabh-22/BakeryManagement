# Bakery Management
This repository holds the code for a Bakery Management System.

## Features

* Inventory Management
* Register and Login
* Get a list of available products
* Place an Order and get the bill
* See order history


## Flow of Project
Customer is required to sign up in order to access the list of all items in inventory or order items. Login/ SignUp will fetch the token for the user which can be used to access the validation API. Once the user has the token, they can send the payload in the request body and get the response in json form according to the logic. Token is to be attached in the headers.

## Flow of logic
>*	Admin can add ingredients and items to the database 
>*	Customers can view all items and order specific items in a quantity
>*	Customers can view their orders
>*	Admin has full access to the inventory and user database

## Paths (local)

* Register: `http://0.0.0.0:8000/register/`

* Login: `http://0.0.0.0:8000/login/`

* All items view API: `http://0.0.0.0:8000/customer/view-items/`

* View all orders API: `http://0.0.0.0:8000/customer/view-orders/`

* Order specific items API: `http://0.0.0.0:8000/customer/order/`

## Staged
The django app is hosted on an EC2 server, hence you can directly check the functionality of the API through there. No auth token is required in this case, the app can be accessed [here](http://18.188.236.213:8000/admin).

```
Admin creds:
username: rishabh
password: qwerty
```

> * Since django has inbuilt an admin panel I haven't made the API for admin part as they can easily be accessed along with a proper front end. 

## Payload
* Order API
```
{
    "item_id": 1,
    "quantity": 2
}
```

* Register
```
{
    "username": "rishabh.",
    "password": "qwerty",
    "age": 23,
    "number": 9540993336,
    "address": "delhi"
}
```

* Login
```
{
    "username": "rishabh.",
    "password": "qwerty"
}
```

# Setup

to run locally: `make`

to run in a container: `make container`

to make Admin: `python manage.py createsuperuser`

> prefer running in a container as running locally will result in installing libraries in your system (instead of a virtual environment).
