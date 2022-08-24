import math, random, os

from flask import render_template, request, abort, redirect, flash, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash

from eventstrolleyapp import app,db
from eventstrolleyapp.models import Admin


@app.route('/admin/login/')
def adminlogin():
        return render_template("admin/login.html")


@app.route('/admin/dashboard/',methods=['GET','POST'])
def admindashboard():
    if request.method == 'GET':
        return redirect('/admin/login/')
    else:
        adminemail = request.form.get('admin_email')
        adminpassword = request.form.get('admin_password')
        if adminemail !='' or adminpassword !='':
            admindeets= db.session.query(Admin).filter(Admin.admin_email==adminemail, Admin.admin_password==adminpassword).first()
            if admindeets:
                session['admin'] = admindeets.admin_id
                return render_template('admin/dashboard.html', admindeets=admindeets)
            else:
                flash('Please ensure the details are correctly filled')
                return redirect('/admin/login/')
        else:
            flash('Please ensure all fields are filled')
            return redirect('/admin/login/', admindeets=admindeets)


@app.route('/admin/dashboard/createticket', methods=['GET','POST'])
def admin_createticket():
    admindeets = session.get('admin')
    if request.method == 'GET':
        return render_template('admin/createticket.html', admindeets=admindeets)
        

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin')
    return redirect('/admin/login/')



