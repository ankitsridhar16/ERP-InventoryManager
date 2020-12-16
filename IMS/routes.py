from flask import  render_template,url_for,redirect,request,flash
from IMS import app,db
from IMS.models import Product,ProductMovement,Location,Balance
from sqlalchemy.exc import IntegrityError


@app.route('/')
def home():
    balance = Balance.query.all()
    return render_template('index.html',balance=balance)

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
        try:
            db.session.add(_product)
            db.session.commit()
            flash(f'{_productName} added successfull !')
            return redirect(url_for('products'))
        except IntegrityError:
            db.session.rollback()
            flash(f'{_productName} already exist')
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
        Balance.query.filter_by(product=_productUpdate.productName).update(dict(product=_productUpdate.productName))
        ProductMovement.query.filter_by(prodName=_productUpdate.productName).update(dict(prodName=_productUpdate.productName))
        try:
            db.session.commit()
            flash(f'{_productUpdate.productName} update successfull !')
            return redirect('/products')
        except IntegrityError:
            db.session.rollback()
            flash(f'{_productUpdate.productName} update unsuccessfull !')
            return redirect('/products')
    else:
        return render_template('updateproduct.html', product=_productUpdate)

@app.route('/deleteproduct/<int:id>')
def delete_product(id):
    _productDelete = Product.query.get_or_404(id)
    try:
        db.session.delete(_productDelete)
        db.session.commit()
        flash(f'{_productDelete.productName} deleted')
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
        try:
            db.session.add(_location)
            db.session.commit()
            flash(f'{_locationName} added successfull !')
            return redirect(url_for('locations'))
        except IntegrityError:
            db.session.rollback()
            flash(f'{_locationName} addition unsuccessfull')
            return redirect(url_for('locations'))
    else:
        locations = Location.query.all()
        return redirect(url_for('locations', locations=locations))


@app.route('/updatelocation/<int:id>', methods=['GET', 'POST'])
def updatelocation(id):
    _updateLocation = Location.query.get_or_404(id)
    if request.method == 'POST':
        _updateLocation.locationName = request.form['location_name']
        _updateLocation.locationAddress = request.form['location_address']
        Balance.query.filter_by(location=_updateLocation.locationName).update(dict(location=_updateLocation.locationName))
        ProductMovement.query.filter_by(fromLocation=_updateLocation.locationName).update(dict(fromLocation=_updateLocation.locationName))
        ProductMovement.query.filter_by(toLocation=_updateLocation.locationName).update(dict(toLocation=_updateLocation.locationName))
        try:
            db.session.commit()
            flash(f'{_updateLocation.locationName} updated successfully !')
            return redirect('/locations')
        except IntegrityError:
            db.session.rollback()
            flash(f'{_updateLocation.locationName} updated unsuccessfull !')
            return redirect('/locations')
    else:
        return render_template('updatelocation.html', location=_updateLocation)

@app.route('/deletelocation/<int:id>')
def deletelocation(id):
    _deleteLocation = Location.query.get_or_404(id)
    try:
        db.session.delete(_deleteLocation)
        flash(f'{_deleteLocation.locationName} deleted !')
        db.session.commit()
        return redirect(url_for('locations'))
    except:
        return redirect(url_for('locations'))



#------------------------------Routes for Transfer - Add,Update and Delete---------------------------#

@app.route('/transfers')
def transfers():
    movements = ProductMovement.query.all()
    return render_template('transfers.html', movements=movements, locations=Location.query.all(), products=Product.query.all())


def validateTransfer(_productName,_productQuantity,_toLocation,_fromLocation):
    _productQuantity = int(_productQuantity)
    if _toLocation == _fromLocation:
        return "error:1"
    
    elif _fromLocation =="Warehouse" and _toLocation != "Warehouse":
        product = Product.query.filter_by(productName=_productName).first()
        if product.productQuantity >= _productQuantity:
            product.productQuantity-= _productQuantity
            balance = Balance.query.filter_by(location=_toLocation,product=_productName).first()
            if(balance==None):
                new = Balance(product=_productName,location=_toLocation,quantity=_productQuantity)
                db.session.add(new)
            else:
                balance.quantity += _productQuantity
            db.session.commit()
        else :
            return False
    elif _toLocation == "Warehouse" and _fromLocation != "Warehouse":
        balance = Balance.query.filter_by(location=_fromLocation,product=_productName).first()
        if(balance==None):
            return 'error:2'
        else:
            if balance.quantity >= _productQuantity:
                product = Product.query.filter_by(productName=_productName).first()
                product.productQuantity += _productQuantity
                balance.quantity -= _productQuantity
                db.session.commit()
            else :
                 return False
    else:
        fromLocationBalance = Balance.query.filter_by(location=_fromLocation,product=_productName).first()
        if(fromLocationBalance== None):
            return "error:2"
        elif fromLocationBalance.quantity > _productQuantity:
            toLocationBalance = Balance.query.filter_by(location=_toLocation,product=_productName).first()
            if toLocationBalance == None:
                newBalance = Balance(product=_productName,location=_toLocation,quantity=_productQuantity)
                db.session.add(newBalance)
                reduceBalance = Balance.query.filter_by(location=_fromLocation,product=_productName).first()
                reduceBalance.quantity -= _productQuantity
                db.session.commit()
            else:
                toLocationBalance.quantity += _productQuantity
                fetchBalance = Balance.query.filter_by(location=_fromLocation,product=_productName).first()
                fetchBalance.quantity -= _productQuantity
                db.session.commit()
        else:
            return False


@app.route('/maketransfer',methods=['POST','GET'])
def maketransfer():
    if request.method == "POST":
        _productName = request.form['product_name']
        _productQuantity = request.form['product_quantity']
        _toLocation = request.form['to_location']
        _fromLocation = request.form['from_location']
        validateRes = validateTransfer(_productName,_productQuantity,_toLocation,_fromLocation)
        if validateRes == "error:1":
            flash(f'Source and destination cannot be the same')
            return redirect(url_for('transfers')) 
        elif validateRes == "error:2":
            flash(f'Source quantity is empty')
            return redirect(url_for('transfers')) 
        elif validateRes == False:
            flash(f'"Put lower quantity"')
            return redirect(url_for('transfers')) 
        else:
            _movement = ProductMovement(fromLocation=_fromLocation, toLocation=_toLocation, prodName=_productName, prodQuantity=_productQuantity) 
            try:
                db.session.add(_movement)
                db.session.commit()
                flash(f'{_movement.prodName} transferred !')
                return redirect(url_for('transfers'))
            except IntegrityError:
                movements = ProductMovement.query.all()
                return redirect(url_for('transfers', movements = movements ))    
    else:
        return redirect(url_for('maketransfer'))

