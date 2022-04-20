import math, random, os

from flask import render_template, request, abort, redirect, flash, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash

from eventstrolleyapp import app,db



@app.route('/')
def homepage():
            return render_template("user/index.html")
        


@app.route('/events/')
def eventspage():
            return render_template("user/events.html")
        
        
        
@app.route('/single/event')
def singleevent():
            return render_template("user/single-event.html")
        

        
@app.route('/blog/')
def blog():
            return render_template("user/blog.html")
        
        

@app.route('/contact/')
def contact():
            return render_template("user/contact.html")