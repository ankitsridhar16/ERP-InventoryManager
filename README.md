# IMS - Inventory Management System

IMS - Inventory Management System is a flask based full stack application to manage inventory products and make transfers based on locations

## Running

Video Demo [link](https://www.youtube.com/watch?v=c0IiuBPqW6o&feature=youtu.be) 

```bash
python3 server.py
```

## Features

### Products:
* Add product price, name and quantity
* Update product
* Delete a product entry

### Locations:
* Create location name and address
* Update location
* Delete a location entry

### Transfers or Movements:
* Add movement with product name, quantity, to and from location


## Updates

* A new model 'balance' establishes a relationship between products,locations and transfers
* Source of transfers/movement are warehouse
* Fixed modal inconsistency
* Validation messages doesnot redirect to new page instead show a flash message on success or       faillure
* Overview , Products and Locations are sorted on basis of product name & location name
* Required modules can be installed from requirements.txt file
