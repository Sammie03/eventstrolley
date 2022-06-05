import datetime, time
from eventstrolleyapp import db
class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_fname = db.Column(db.String(255), nullable=False)
    admin_lname = db.Column(db.String(255), nullable=False)
    admin_email = db.Column(db.String(255), nullable=False, unique=True)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)

class Customer(db.Model): 
    customer_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    customer_fname = db.Column(db.String(255), nullable=False)
    customer_lname = db.Column(db.String(255), nullable=False)
    customer_phone = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False, unique=True)
    customer_pword = db.Column(db.String(255), nullable=False)
    customer_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)
    
class Vendor(db.Model): 
    vendor_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    vendor_fname = db.Column(db.String(255), nullable=False)
    vendor_lname = db.Column(db.String(255), nullable=False)
    vendor_business_name = db.Column(db.String(255), nullable=False)
    fk_location_state_id = db.Column(db.Integer(), db.ForeignKey("state.state_id"))
    vendor_phone = db.Column(db.String(255), nullable=False)
    vendor_email = db.Column(db.String(255), nullable=False, unique=True)
    vendor_pword = db.Column(db.String(255), nullable=False)
    vendor_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)

class State(db.Model):
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)
    
class Lga(db.Model):
    lga_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    lga_name = db.Column(db.String(255), nullable=False)
    #foreign key
    fk_state_id = db.Column(db.Integer(), db.ForeignKey("states.state_id"))
    
class Ticket(db.Model):
    ticket_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    ticket_desc = db.Column(db.String(255), nullable=False)
    ticket_venue = db.Column(db.String(255), nullable=False)
    venue_address = db.Column(db.String(255), nullable=False)
    event_time = db.Column(db.Time(), nullable=False)
    event_start_date = db.Column(db.Date(), nullable=False)
    event_end_date = db.Column(db.Date(), nullable=False)
    fk_event_categories = db.Column(db.Integer(), db.ForeignKey("Categories.categories_id"))
    ticket_sales_start_date = db.Column(db.Date(), nullable=False)
    ticket_sales_end_date = db.Column(db.Date(), nullable=False)
    ticket_type = db.Column(db.String(255), nullable=False)
    ticket_price = db.Column(db.Float(), nullable=False)
    ticket_desc = db.Column(db.String(255), nullable=False)
    no_of_tickets = db.Column(db.Integer(), nullable=True)
    payment_type = db.Column(db.Enum('Paid','Free'))
    
class Payment(db.Model):
    payment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    payment_amount = db.Column(db.Float(), nullable=False)
    payment_status = db.Column(db.Enum('Successful','Failed'))
    payment_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    payment_method = db.Column(db.String(255), nullable=False)
    payment_ref = db.Column(db.String(255), nullable=False)
    fk_payment_ticket_id = db.Column(db.Integer(), db.ForeignKey("ticket.ticket_id"))

class Subscribers(db.Model):
    subscribers_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    subscribers_email = db.Column(db.String(255), nullable=False)