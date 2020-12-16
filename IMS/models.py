from IMS import db
from datetime import datetime



#------------------------------------------------------------------------------------------#
# ORM's for our models

# Product model database table
class Product(db.Model):
    productId = db.Column(db.Integer, primary_key= True)
    productName = db.Column(db.String(50),unique = True ,nullable = False)
    productPrice= db.Column(db.Integer,nullable = False)
    productQuantity = db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return f"Product('{self.productId}','{self.productName}','{self.productQuantity}')"

# Location model database table
class Location(db.Model):
    locationId = db.Column(db.Integer, primary_key= True)
    locationName = db.Column(db.String(20),unique = True, nullable = False)
    locationAddress = db.Column(db.String(50), nullable = False)
    def __repr__(self):
        return f"Location('{self.locationId}','{self.locationName}','{self.locationAddress}')"

# Product Movement database table       
class ProductMovement(db.Model):
    movementId = db.Column(db.Integer, primary_key= True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fromLocation = db.Column(db.String(20), nullable = False)
    toLocation = db.Column(db.String(20), nullable = False)
    prodName = db.Column(db.String(20), nullable = False)
    prodQuantity = db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return f"Movement('{self.movementId}','{self.timestamp}','{self.fromLocation}','{self.toLocation}','{self.prodName}','{self.prodQuantity}')"

# Balance Database table to maintain realtionship between location & products
class Balance(db.Model):
    balanceId = db.Column(db.Integer, primary_key= True,nullable = False)
    product = db.Column(db.String(20), nullable = False)
    location = db.Column(db.String(20),nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Balance('{self.balanceId}','{self.product}','{self.location}','{self.quantity}')"