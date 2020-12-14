from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IMS.db'
app.secret_key = '2540'
db = SQLAlchemy(app)


from IMS import routes
db.create_all()
db.session.commit()