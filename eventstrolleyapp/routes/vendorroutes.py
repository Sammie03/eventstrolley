import math
import random
import os
import requests
import json
from flask import make_response, render_template, request, abort, redirect, flash, session
from sqlalchemy import desc
from eventstrolleyapp import app, db
from eventstrolleyapp.models import Vendor, State, Ticket
# from easetestprojapp.forms import LoginForm


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

# @app.route('/user/settings')
# def user_settings():
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         custdeets = Customer.query.get(loggedin)
#         return render_template('user/usersettings.html', custdeets=custdeets)


# @app.route('/user/update/<id>', methods=['POST'])
# def user_update(id):
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         fname = request.form.get('fname')
#         lname = request.form.get('lname')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         img = request.files.get('img')

#         original_file = img.filename
#         extension = os.path.splitext(original_file)
#         fn = math.ceil(random.random() * 100000000)
#         save_as = str(fn) + extension[1]
#         if extension[1].lower() in ['.jpg', '.png', '.jpeg', '.webp', '.svg']:
#             img.save(f'easetestprojapp/static/user_images/{save_as}')

#         if int(loggedin) == int(id):
#             c = Customer.query.get(id)
            
#             c.cust_fname = fname
#             c.cust_lname = lname
#             c.cust_email = email
#             c.cust_phone = phone
#             c.cust_img = save_as
#             db.session.add(c)
#             db.session.commit()

#         flash('Changes Made Successfully')
#         return redirect('/userdashboard')


@app.route('/vendor/logout')
def vendor_logout():
    vendor_loggedin = session.get('vendor_loggedin')
    if vendor_loggedin == None:
        return redirect('/')
    else:
        session.pop('vendor_loggedin')
        return redirect('/vendor/login')



# @app.route('/')
# def home():
#     all_salons = Salon.query.filter(Salon.salon_status == '1').limit(3)
#     service_type = Service_type.query.all()
#     servs51 = Service_type.query.limit(5)
#     servs52 = Service_type.query.order_by(desc( Service_type.servtype_id)).limit(5)
#     recent_sals = Salon.query.filter(Salon.salon_status == '1').order_by(desc(Salon.salon_id)).order_by(Salon.salon_name).limit(3)
#     salon_loggedin = session.get('salon_loggedin')
#     salondeets = Salon.query.get(salon_loggedin)
#     # all_salons = Salon.query.order_by(desc(Salon.salon_id))
#     return render_template('user/home.html', cust_deets=cust_deets, all_salons=all_salons, service_type=service_type, recent_sals=recent_sals,salondeets=salondeets, servs51=servs51, servs52=servs52)


# @app.route('/vendor/signup')
# def signup():
#     vendor_loggedin = session.get('vendor_loggedin')
#     # vendor_deets = Vendor.query.get(vendor_loggedin)
#     return render_template('vendor/signup.html')


# @app.route('/signup/submit', methods=['POST'])
# def signup_submit():
#     fname = request.form.get('fname')
#     lname = request.form.get('lname')
#     email = request.form.get('email')
#     pwd = request.form.get('pwd')
#     confpwd = request.form.get('confpwd')
#     gender = request.form.get('gender')
#     vals = request.form.values()

#     chkEmail = Customer.query.filter(Customer.cust_email==email).first()

#     if '' in vals:
#         flash('Please complete all fields')
#         return redirect('/signup')
#     elif pwd != confpwd:
#         flash('Please make sure both passwords are the same')
#         return redirect('/signup')
#     elif chkEmail:
#         flash('This Email is taken')
#         return redirect('/salon/signup')
#     else:
#         c = Customer(cust_fname=fname, cust_lname=lname,
#                      cust_email=email, cust_pwd=pwd, cust_gender=gender)

#         db.session.add(c)
#         db.session.commit()

#         id = c.cust_id
#         session['loggedin'] = id

#         flash('Registration Successful')
#         return redirect('/userdashboard')


# @app.route('/userdashboard')
# def userdash():
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         custdeets = Customer.query.get(loggedin)
#         return render_template('user/userdashboard.html', custdeets=custdeets)


# @app.route('/user/login', methods=['POST', 'GET'])
# def user_login():
#     if request.method == 'GET':
#         return render_template('user/login.html')
#     else:
#         username = request.form.get('username')
#         pwd = request.form.get('pwd')
#         if username != '' and pwd != '':
#             deets = Customer.query.filter(
#                 Customer.cust_email == username, Customer.cust_pwd == pwd).first()
#             if deets:
#                 id = deets.cust_id
#                 session['loggedin'] = id
#                 return redirect('/userdashboard')
#             else:
#                 flash('Invalid Credentials')
#                 return redirect('/user/login')
#         else:
#             flash('Please complete all fields')
#             return redirect('/user/login')


# @app.route('/user/settings')
# def user_settings():
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         custdeets = Customer.query.get(loggedin)
#         return render_template('user/usersettings.html', custdeets=custdeets)


# @app.route('/user/update/<id>', methods=['POST'])
# def user_update(id):
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         fname = request.form.get('fname')
#         lname = request.form.get('lname')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         img = request.files.get('img')

#         original_file = img.filename
#         extension = os.path.splitext(original_file)
#         fn = math.ceil(random.random() * 100000000)
#         save_as = str(fn) + extension[1]
#         if extension[1].lower() in ['.jpg', '.png', '.jpeg', '.webp', '.svg']:
#             img.save(f'easetestprojapp/static/user_images/{save_as}')

#         if int(loggedin) == int(id):
#             c = Customer.query.get(id)
            
#             c.cust_fname = fname
#             c.cust_lname = lname
#             c.cust_email = email
#             c.cust_phone = phone
#             c.cust_img = save_as
#             db.session.add(c)
#             db.session.commit()

#         flash('Changes Made Successfully')
#         return redirect('/userdashboard')


# @app.route('/logout')
# def logout():
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         session.pop('loggedin')
#         return redirect('/')


# @app.route('/about')
# def about():
#     loggedin = session.get('loggedin')
#     custdeets = Customer.query.get(loggedin)
#     return render_template('user/about.html', custdeets=custdeets)


# @app.route('/layout')
# def layout():
#     loggedin = session.get('loggedin')
#     cust_deets = Customer.query.get(loggedin)
#     return render_template('user/layout.html', cust_deets=cust_deets)


# @app.route('/book/salon/<id>', methods=['POST', 'GET'])
# def book_salon(id):
#     loggedin = session.get('loggedin')
    
#     if loggedin == None:
#         return redirect('/user/login')
#     else:    
#         if request.method == 'GET':
#             all_salons = Salon.query.get(id)
#             servs = Service.query.filter(Service.serv_salonid == id).all()
#             cust_deets = Customer.query.get(loggedin)
#             return render_template('user/booksalon.html', all_salons=all_salons, servs=servs, cust_deets=cust_deets)
#         else:
#             s = Salon.query.get(id)
#             cust = Customer.query.get(loggedin)

#             # bserv_bookid	bserv_servid

#             date = request.form.get('date')
#             time = request.form.get('time')
#             servs = request.form.getlist('services')

#             b = Booking(book_salonid=s.salon_id, book_custid=loggedin,
#                         book_date=date, book_time=time)
#             db.session.add(b)
#             db.session.commit()

#             for v in servs:
#                 bserv = Book_service(bserv_bookid=b.book_id, bserv_servid=v)
#                 db.session.add(bserv)
#             db.session.commit()

#             bookid = b.book_id
#             session['booked'] = bookid

#             # bserv = Book_service(bserv_bookid=b.book_id)

#             # bservid = bserv.bserv_id
#             # session['bserved'] = bservid

#             # id = c.cust_id
#             # session['loggedin'] = id

#             return redirect('/booking/summary')


# @app.route('/booking/summary', methods=['POST', 'GET'])
# def booking_sum():
#     loggedin = session.get('loggedin')
#     cust_deets = Customer.query.get(loggedin)

#     booked = session.get('booked')
#     bookdeets = Booking.query.get(booked)

#     # bserved = session.get('bserved')
#     # get_bserved = Book_service.query.get(bserved)

#     # allmy_servs = Service.query.all()

#     bservdeets = Book_service.query.filter(
#         Book_service.bserv_bookid == bookdeets.book_id).all()
#     # bserv_service = Book_service.query.filter(get_bserved.bserv_servid==allmy_servs.serv_id).all()
#     refno = math.ceil(random.random() * 1000000000)

#     if loggedin == None:
#         return redirect('/user/login')
#     else:
#         if request.method == 'GET':
#             return render_template('user/booksummary.html', cust_deets=cust_deets, bookdeets=bookdeets, bservdeets=bservdeets)
#         else:
#             tot = request.form.get('tot')

#             for bs in bservdeets:
#                 bkpay = Book_pay(bookpay_amt=tot, bookpay_ref=refno,
#                                  bookpay_bookservid=bs.bserv_id,bookpay_bookcustid=loggedin,bookpay_booksalonid=bookdeets.book_salonid)
#                 db.session.add(bkpay)
#             db.session.commit()

#             p = Payment(pay_amt=tot, pay_refno=refno, pay_stat='completed',pay_salonid=bookdeets.book_salonid,pay_custid=loggedin, pay_bookid=bookdeets.book_id)
#             db.session.add(p)
#             db.session.commit()

#             session['ref'] = refno
#             return redirect('/user/payment')


# @app.route('/user/payment')
# def user_payment():
#     loggedin = session.get('loggedin')
#     custdeets = Customer.query.get(loggedin)

#     booked = session.get('booked')
#     bookdeets = Booking.query.get(booked)

#     refnum = session.get('ref')

#     bservdeets = Book_service.query.filter(
#         Book_service.bserv_bookid == bookdeets.book_id).all()
#     bservdeets2 = Book_service.query.filter(
#         Book_service.bserv_bookid == bookdeets.book_id).first()

#     bpaydeets = Book_pay.query.filter(
#         Book_pay.bookpay_bookservid == Book_service.bserv_id).first()

#     amtdeets = Book_pay.query.filter(Book_pay.bookpay_ref == refnum).first()

#     if loggedin == None or refnum == None or amtdeets == None:
#         return redirect('/')
#     else:
#         if request.method == 'GET':
#             return render_template('user/payment.html', custdeets=custdeets, bservdeets=bservdeets, bservdeets2=bservdeets2, bpaydeets=bpaydeets, refnum=refnum, amtdeets=amtdeets)
#         else:   

#             url = "https://api.paystack.co/transaction/initialize"

#             data = {'email': custdeets.cust_email,
#                     'amount': amtdeets.bookpay_amt, 'ref': amtdeets.bookpay_ref, 'status':'Transaction Completed'}

#             headers = {'Content-Type': 'application/json',
#                        'Authorization': 'Bearer sk_test_cd05140387131fa0a4b595e1a7d8a2b1b9ae6b76'}

#             response = requests.post(
#                 'https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

#             rspjson = json.loads(response.text)
#             if rspjson.get('status') == True:
               
#                 authurl = rspjson['data']['authorization_url']

#                 return redirect(authurl)   
#             else:
#                 return 'Please try again'



# @app.route('/user/confirmpay')
# def confirm_pay():
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         cust_deets = Customer.query.get(loggedin)
#         return render_template('user/confirmpay.html', cust_deets=cust_deets)


# @app.route('/user/dashboard/payment')
# def dashboard_payment():
#     loggedin = session.get('loggedin')
#     custdeets = Customer.query.get(loggedin)
#     if loggedin == None:
#         return redirect('/')
#     else:
#         paydeets = Book_pay.query.filter(Book_pay.bookpay_bookcustid==loggedin).all()

#         return render_template('user/userpayment_dashboard.html', paydeets=paydeets, custdeets=custdeets)



# @app.route('/user/bookings')
# def user_bookings():
#     loggedin = session.get('loggedin')
#     if loggedin == None:
#         return redirect('/')
#     else:
#         custdeets = Customer.query.get(loggedin)
#         b = Booking.query.filter(Booking.book_custid == loggedin).all()
#         msg = 'You have not booked for a salon yet. Book now to enjoy the best service you can get, while also qualifying for bonuses and other benefits.'
#         return render_template('user/userbookings.html', b=b, custdeets=custdeets, msg=msg)


# @app.route('/user/services')
# def user_services():
#     loggedin = session.get('loggedin')
#     cust_deets = Customer.query.get(loggedin)
#     return render_template('user/services.html', cust_deets=cust_deets)


# @app.route('/all/salons')
# def all_salons():
#     loggedin = session.get('loggedin')
#     cust_deets = Customer.query.get(loggedin)
#     all_salons = Salon.query.order_by(Salon.salon_name)
#     return render_template('user/allsalons.html', cust_deets=cust_deets, all_salons=all_salons)


# @app.route('/user/search', methods=['GET','POST'])
# def user_search():
#     loggedin = session.get('loggedin')
#     cust_deets = Customer.query.get(loggedin)

#     if request.method=='GET':
#         return redirect('/')
#     else:
#         locationdrop = request.form.get('locationdrop')
#         servicedrop = request.form.get('servicedrop')

#         locationsearch = '%{}%'.format(locationdrop)
    
#         filterstr = ''
  
#         # filterstr = filterstr + (Salon.salonobj_serv.servtypeserv.servtype_id==servicedrop)
#         # filterstr = filterstr + (Service_type.servtype_id==servicedrop)
        

#         # if locationdrop != '':
#         #     filterstr = filterstr + (Salon.salon_address.like(locationsearch))
#         #     loc_res = db.session.query(Salon).filter(filterstr).all()

#         if servicedrop != '':
#             serv_res = Service_type.query.filter(Service_type.servtype_id==servicedrop).all()
           
          
#         # elif servicedrop == '' and locationdrop != '':
#         #     s
#         # elif  locationdrop != '' and servicedrop != '':
#         #     filterstr = filterstr + (Salon.salon_address.like(locationsearch))
#         #     all_res = db.session.query(Salon).filter(filterstr).Service_type.query.filter(Service_type.servtype_id==servicedrop).all()

#         return render_template('user/starter.html', cust_deets=cust_deets, serv_res=serv_res, servicedrop=servicedrop,locationdrop=locationdrop)


# @app.route('/user/dashboard/<id>')
# def user_dashboard(id):
#     loggedin = session.get('loggedin')
#     cust_deets = Customer.query.get(loggedin)

#     if loggedin == None:
#         return redirect('/')
#     else:
#         return render_template('/')

# # @app.route('/user/layout')
# # def user_layout():
# #     loggedin = session.get('loggedin')
# #     cust_deets = Customer.query.get(loggedin)

# #     return render_template('user/layout.html',cust_deets=cust_deets)

