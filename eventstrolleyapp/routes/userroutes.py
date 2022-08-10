import math, random, os

from flask import render_template, request, abort, redirect, flash, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash

from eventstrolleyapp import app,db
from eventstrolleyapp.models import Admin, Customer, Guest, Vendor


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
            return render_template("user/contact.html")



@app.route('/register/', methods=['GET','POST'])
def register():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if request.method == 'GET':
        return render_template('/user/signup.html', userdeets=userdeets)
    else:
        email = request.form.get('email')
        pswd1 = request.form.get('pswd1')
        pswd2 = request.form.get('pswd2')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')

        userdeets2 = userdeets = Customer.query.filter(Customer.customer_email==email).first()

        #validate
        if email == '' or pswd1 == '' or firstname == '' or lastname == '' or pswd2 == '':
            flash('Registration failed, kindly fill the required fields', 'warning')
            return redirect ('/register')
        elif userdeets2:
            flash('Email already exists', 'warning')
            return redirect ('/register')
        elif pswd1 != pswd2:
            flash('Kindly ensure that the passwords match', 'warning')
            return redirect ('/register')
        else:
            formated = generate_password_hash(pswd1)
            flash('Registration successful', 'success')
            profile = Customer(customer_email = email, customer_pword = formated, customer_fname = firstname, customer_lname = lastname, customer_phone = phone)
            db.session.add(profile)
            db.session.commit()
            user = profile.customer_id
            session['loggedin'] = user
            return redirect('/login')



@app.route('/login/', methods=['GET','POST'])
def login():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if request.method == 'GET':
        return render_template('/user/login.html', userdeets=userdeets)
    else:
        email = request.form.get('email')
        pswd = request.form.get('pswd')

        if email == '' or pswd == '':
            flash('Your email or password is incorrect. Please check and try and again', 'warning')
            return redirect('/login')
        else:
            userdeets = Customer.query.filter(Customer.customer_email==email).first()
            formated_password =  userdeets.customer_pword
            check_password = check_password_hash(formated_password,pswd)

            if check_password == True:
                session['loggedin'] = userdeets.customer_id
                return redirect ('/profile')
            else:
                flash('Invalid login credentials', 'warning')
                return redirect ('/')



@app.route('/profile/', methods=['GET','POST'])
def user():
    user = session.get('loggedin')
    userdeets =  Customer.query.get(user)
    if user == None:
        return redirect('/login')
    else:
        return render_template ('/user/userdashboard.html', userdeets=userdeets )



@app.route('/logout')
def logout():
    user = session.get('loggedin')
    if user == None:
        return redirect ('/')
    else:
        session.pop('loggedin')
        return redirect ('/') 
