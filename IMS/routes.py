from flask import  render_template,url_for,redirect,request
from IMS import app,db
from IMS.models import Product,ProductMovement,Location



@app.route('/')
def home():
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('index.html',products=products,locations=locations)

# ---------------------------Product Routes - Add, Update, Delete---------------------------#
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products, locations=Location.query.all())

@app.route('/addproduct',methods=['POST','GET'])
def addproduct():
    if request.method == "POST":
        _productName = request.form['product_name']
        _productPrice = request.form['product_price']
        _productQuantity = request.form['product_quantity']
        _product = Product(productName=_productName,productPrice=_productPrice,productQuantity=_productQuantity)
        print(_product)
        try:
            db.session.add(_product)
            db.session.commit()
            return redirect(url_for('products'))
        except:
            return 'Adding product unsuccessful'
    else:
        products = Product.query.all()
        return redirect(url_for('products', products=products))

@app.route('/updateproduct/<int:product_id>', methods=['GET','POST'])
def updateproduct(product_id):
    _productUpdate = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        _productUpdate.productName = request.form['product_name']
        _productUpdate.productPrice = request.form['product_price']
        _productUpdate.productQuantity = request.form['product_quantity']
        try:
            db.session.commit()
            return redirect('/products')
        except:
            return "Update Product Unsucceflu"
    else:
        return render_template('updateproduct.html', product=_productUpdate)

@app.route('/deleteproduct/<int:id>')
def delete_product(id):
    _productDelete = Product.query.get_or_404(id)
    try:
        db.session.delete(_productDelete)
        db.session.commit()
        return redirect(url_for('products'))
    except:
        return redirect(url_for('products'))


#------------------------------Routes for locations-Add,Update,Delete-------------------------#
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html',locations=locations)

@app.route('/addlocation',methods=['POST','GET'])
def addlocation():
    if request.method == "POST":
        _locationName = request.form['location_name']
        _locationAddress = request.form['location_address']
        _location = Location(locationName=_locationName,locationAddress=_locationAddress)
        print(_location)
        try:
            db.session.add(_location)
            db.session.commit()
            return redirect(url_for('locations'))
        except:
            return "Add Location went wrong!"
    else:
        locations = Location.query.all()
        return redirect(url_for('locations', locations=locations))


@app.route('/updatelocation/<int:id>', methods=['GET', 'POST'])
def updatelocation(id):
    _updateLocation = Location.query.get_or_404(id)
    if request.method == 'POST':
        _updateLocation.locationName = request.form['location_name']
        _updateLocation.locationAddress = request.form['location_address']
        try:
            db.session.commit()
            return redirect('/locations')
        except:
            return "Update location unsuccessfull"
    else:
        return render_template('updatelocation.html', location=_updateLocation)

@app.route('/deletelocation/<int:id>')
def deletelocation(id):
    _deleteLocation = Location.query.get_or_404(id)
    try:
        db.session.delete(_deleteLocation)
        db.session.commit()
        return redirect(url_for('locations'))
    except:
        return redirect(url_for('locations'))



#------------------------------Routes for Transfer - Add,Update and Delete---------------------------#

@app.route('/transfers')
def transfers():
    movements = ProductMovement.query.all()
    return render_template('transfers.html', movements=movements, locations=Location.query.all(), products=Product.query.all())

@app.route('/maketransfer',methods=['POST','GET'])
def maketransfer():
    if request.method == "POST":
        _productName = request.form['product_name']
        _productQuantity = request.form['product_quantity']
        _toLocation = request.form['to_location']
        _fromLocation = request.form['from_location']
        if _toLocation == _fromLocation:
            return "To and From location cannot be the same"
        _movement = ProductMovement(fromLocation=_fromLocation, toLocation=_toLocation, prodName=_productName, prodQuantity=_productQuantity)   
        try:
            db.session.add(_movement)
            db.session.commit()
            return redirect(url_for('transfers'))
        except:
            movements = ProductMovement.query.all()
            return redirect(url_for('transfers', movements = movements ))
        
    else:
        return redirect(url_for('productmovement'))

@app.route('/updatetransfer/<int:id>', methods=['GET', 'POST'])
def updatetransfer(id):
    _updateMovement = ProductMovement.query.get_or_404(id)
    if request.method == 'POST':
        _updateMovement.prodName = request.form['product_name']
        _updateMovement.prodQuantity = request.form['product_quantity']
        _updateMovement.toLocation = request.form['to_location']
        _updateMovement.fromLocation = request.form['from_location']
        if _updateMovement.toLocation == _updateMovement.fromLocation:
            return "To and From location cannot be the same"
        try:
            db.session.commit()
            return redirect(url_for('transfers'))
        except:
            return "Update Transfer Unsuccesfull"
    else:
        return render_template('updatetransfer.html', movement=_updateMovement, locations=Location.query.all())


@app.route('/deletetransfer/<int:id>')
def deletetransfer(id):
    _deleteMovement = ProductMovement.query.get_or_404(id)
    try:
        db.session.delete(_deleteMovement)
        db.session.commit()
        return redirect(url_for('transfers'))
    except:
        return redirect(url_for('transfers'))
