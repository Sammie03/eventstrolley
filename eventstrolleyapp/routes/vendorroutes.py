import math
import random
import os
import json
from flask import make_response, render_template, request, abort, redirect, flash, session
from sqlalchemy import desc
from eventstrolleyapp import app, db
from eventstrolleyapp.models import Vendor, State, Ticket



@app.route('/vendor/signup')
def vendor_signup():
    vendor_loggedin = session.get('vendor_loggedin')
    vendor_deets = Vendor.query.get(vendor_loggedin)
    return render_template('vendor/signup.html')

@app.route('/vendor/signup/submit', methods=['POST'])
def vendor_signup_submit():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    number = request.form.get('number')
    pwd = request.form.get('pwd')
    pwdagain = request.form.get('pwdagain')
    vals = request.form.values()

    chkEmail = Vendor.query.filter(Vendor.vendor_email==email).first()

    if '' in vals:
        flash('Please complete all fields')
        return redirect('/vendor/signup')
    elif pwd != pwdagain:
        flash('Please make sure both passwords are the same')
        return redirect('/vendor/signup')
    elif chkEmail:
        flash('This Email is taken')
        return redirect('/vendor/signup')
    else:
        v = Vendor(vendor_fname=fname, vendor_lname=lname,
                     vendor_email=email, vendor_phone=number, vendor_pword=pwd)

        db.session.add(v)
        db.session.commit()

        id = v.vendor_id
        session['loggedin'] = id

        flash('Registration Successful')
        return redirect('/vendor/login')


@app.route('/vendor/login', methods=['GET','POST'])
def vendor_login():
    if request.method == 'GET':
        return render_template('vendor/login.html')
    else:
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        if email != '' and pwd != '':
            deets = Vendor.query.filter(
                Vendor.vendor_email == email, Vendor.vendor_pword == pwd).first()
            if deets:
                id = deets.vendor_id
                session['vendor_loggedin'] = id
                flash('Login Successful')
                return redirect('/vendor/dashboard')
            else:
                flash('Invalid Credentials')
                return redirect('/vendor/login')
        else:
            flash('Please complete all fields')
            return redirect('/vendor/login')


@app.route('/vendor/dashboard')
def vendor_dashboard():
    vendor_loggedin = session.get('vendor_loggedin')
    if vendor_loggedin == None:
        return redirect('/')
    else:
        vendor_deets = Vendor.query.get(vendor_loggedin)
        return render_template('vendor/dashboard.html', vendor_deets=vendor_deets)


@app.route('/vendor/logout')
def vendor_logout():
    vendor_loggedin = session.get('vendor_loggedin')
    if vendor_loggedin == None:
        return redirect('/')
    else:
        session.pop('vendor_loggedin')
        return redirect('/vendor/login')




