from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

#Instantiate an object of Flask
app = Flask(__name__, instance_relative_config=True)
csrf=CSRFProtect(app)



#Local imports starts here
from eventstrolleyapp import config 
app.config.from_object(config.ProductionConfig)
app.config.from_pyfile('config.py',silent=False)

db = SQLAlchemy(app)

#Load your routes here
from eventstrolleyapp.routes import adminroutes, userroutes, vendorroutes
from eventstrolleyapp import forms 
from eventstrolleyapp import models