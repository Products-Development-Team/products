# NYU DevOps Project-- Product Team

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://github.com/Products-Development-Team/products/actions/workflows/tdd.yml/badge.svg)](https://github.com/Products-Development-Team/products/actions)
[![Build Status](https://github.com/Products-Development-Team/products/actions/workflows/bdd.yml/badge.svg)](https://github.com/Products-Development-Team/products/actions)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is an NYU DevOps project that creates a RESTful microservice using Python Flask and PostgreSQL. 

## Prerequisite Software Installation
This project uses Docker and VS Code with the Remote Containers extension to provide a consistent repeatable disposable development environment. 

You will need the following software installed: 
- Docker Desktop
- VS Code
- Remote Containers extension from the VS Code Marketplace

## Bring up development environment
To bring up the development environment you should clone this repo, change into the repo directory, and then open Visual Studio Code using the code . command. VS Code will prompt you to reopen in a container and you should select it. This will take a while the first time as it builds the Docker image and creates a container from it to develop in.

```bash
git clone git@github.com:Products-Development-Team/products.git
cd products
code .
```

## Running the tests
You can run the tests in a ```bash``` terminal using the following command: 
```bash
make test
```
This will run the test suite and report the code coverage. 

## Check PEP8 Standard
We've included flake8, Pylint and Black in the ```requirements.txt```, you can check if the code is compliant using the following command: 
```bash
make lint
```

## Run the REST service
To run the service, use the same ```bash``` terminal that you ran the tests in and use 
```bash
honcho start
``` 
(Press CTRL+C to exit).
You should be able to open a web page in a local browser at: http://localhost:8000

## Make REST calls
While the service is running, you can open a second ``bash`` terminal and issue the following commands: 

List all resources (Root URL):
```bash
http GET http://localhost:8000/
```
List all products: 
```bash
http GET http://localhost:8000/products
```
Create a product: 
```bash
http POST localhost:8000/products name="" description="" category="" price:=<float> available:=<bool> rating:=<int>
```
You must specifiy the ``name``, ``description``, ``category``, ``price`` and ``rating``of the product. 
- Acceptable price is within range: ``10.0-100.0``
- Acceptable rating is between ``0-5``

Read a product:
```bash
http GET localhost:8000/products/<int:product_id>
```
Update a product: 
```bash
http PUT localhost:8000/products/<int:product_id>
```
Delete a product: 
```bash
http DELETE localhost:8000/products/<int:product_id>
```

## What's featured in the project? 
* app/routes.py -- the main Service routes using Python Flask
* app/models.py -- the data model using SQLAlchemy
* tests/test_routes.py -- test cases against the Product service
* tests/test_models.py -- test cases against the Product model
## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
