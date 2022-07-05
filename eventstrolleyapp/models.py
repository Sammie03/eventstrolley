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

    #relationship
    ticketholder_customer = db.relationship('TicketHolder', back_populates ='customer_ticketholder')
    payment_customer = db.relationship('Payment', back_populates ='customer_payment')


class Guest(db.Model): 
    guest_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    guest_fname = db.Column(db.String(255), nullable=False)
    guest_lname = db.Column(db.String(255), nullable=False)
    guest_phone = db.Column(db.String(255), nullable=False)
    guest_email = db.Column(db.String(255), nullable=False, unique=True)
    guest_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)

    #relationship
    ticketholder_guest = db.relationship('TicketHolder', back_populates ='guest_ticketholder')
    payment_guest = db.relationship('Payment', back_populates ='guest_payment')


    
class Vendor(db.Model): 
    vendor_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    vendor_fname = db.Column(db.String(255), nullable=False)
    vendor_lname = db.Column(db.String(255), nullable=False)
    vendor_phone = db.Column(db.String(255), nullable=False)
    vendor_email = db.Column(db.String(255), nullable=False, unique=True)
    vendor_pword = db.Column(db.String(255), nullable=False)
    vendor_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #foreignkey
    fk_location_state_id = db.Column(db.Integer(), db.ForeignKey("state.state_id"))

    #relationship
    ticket_vendor = db.relationship('Ticket', back_populates ='vendor_ticket')
    state_vendor = db.relationship('State', back_populates ='vendor_state')


class State(db.Model):
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)
    
    #relationship
    vendor_state = db.relationship('Vendor', back_populates ='state_vendor')
    lga_state = db.relationship('Lga', back_populates ='state_lga')
    ticket_state = db.relationship('Ticket', back_populates ='state_ticket')


class Lga(db.Model):
    lga_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    lga_name = db.Column(db.String(255), nullable=False)
    #foreign key
    fk_state_id = db.Column(db.Integer(), db.ForeignKey("state.state_id"))

    #relationship
    state_lga = db.relationship('State', back_populates ='lga_state')
    ticket_lga = db.relationship('Ticket', back_populates ='lga_ticket')



class Tickettype(db.Model):
    tickettype_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    tickettype__name = db.Column(db.String(255), nullable=False)
    ticketprice = db.Column(db.Float(), nullable=False)

    #foreign key
    fk_ticket_id = db.Column(db.Integer(), db.ForeignKey("ticket.ticket_id"))

    #relationship
    ticketholder_type = db.relationship('TicketHolder', back_populates ='tickettype_holder')



# class Ticketprice(db.Model):
#       ticketprice_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
#       ticketprice = db.Column(db.Float(), nullable=False)

#     #foreign key
#       fk_ticket_id = db.Column(db.Integer(), db.ForeignKey("Ticket.ticket_id"))



class Categories(db.Model):
    categories_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    categories_name = db.Column(db.String(255), nullable=False)

    #relationship
    ticket_categories = db.relationship('Ticket', back_populates ='categories_ticket')



class TicketHolder(db.Model):
    ticketholder_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    event_name = db.Column(db.String(255), nullable=False)
    ticket_desc = db.Column(db.String(255), nullable=False)
    event_venue = db.Column(db.String(255), nullable=False)
    venue_address = db.Column(db.String(255), nullable=False)
    event_time = db.Column(db.Time(), nullable=False)

    # foreign keys
    fk_ticket_id = db.Column(db.Integer(), db.ForeignKey("ticket.ticket_id"))
    fk_guest_id = db.Column(db.Integer(), db.ForeignKey("guest.guest_id"))
    fk_customer_id = db.Column(db.Integer(), db.ForeignKey("customer.customer_id"))
    fk_tickettype = db.Column(db.Integer(), db.ForeignKey("tickettype.tickettype_id"))

    #relationship
    customer_ticketholder = db.relationship('Customer', back_populates ='ticketholder_customer')
    guest_ticketholder = db.relationship('Guest', back_populates ='ticketholder_guest')
    tickettype_holder = db.relationship('Tickettype', back_populates ='ticketholder_type')
    ticket = db.relationship('Ticket', back_populates ='ticket_holder')




class Ticket(db.Model):
    ticket_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    event_name = db.Column(db.String(255), nullable=False)
    ticket_desc = db.Column(db.String(255), nullable=False)
    event_venue = db.Column(db.String(255), nullable=False)
    venue_address = db.Column(db.String(255), nullable=False)
    event_time = db.Column(db.Time(), nullable=False)
    event_start_date = db.Column(db.Date(), nullable=False)
    event_end_date = db.Column(db.Date(), nullable=False)
    ticket_sales_start_date = db.Column(db.Date(), nullable=False)
    ticket_sales_end_date = db.Column(db.Date(), nullable=False)
    no_of_tickets = db.Column(db.Integer(), nullable=True)
    payment_type = db.Column(db.Enum('Paid','Free'))

    # foreign keys
    fk_categories = db.Column(db.Integer(), db.ForeignKey("categories.categories_id"))
    fk_vendor = db.Column(db.Integer(), db.ForeignKey("vendor.vendor_id"))
    fk_state = db.Column(db.Integer(), db.ForeignKey("state.state_id"))
    fk_lga = db.Column(db.Integer(), db.ForeignKey("lga.lga_id"))

    #relationship
    vendor_ticket = db.relationship('Vendor', back_populates ='ticket_vendor')
    state_ticket = db.relationship('State', back_populates ='ticket_state')
    lga_ticket = db.relationship('Lga', back_populates ='ticket_lga')
    categories_ticket = db.relationship('Categories', back_populates ='ticket_categories')
    ticket_holder = db.relationship('TicketHolder', back_populates ='ticket')


class Payment(db.Model):
    payment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    payment_status = db.Column(db.Enum('Successful','Failed','Pending'))
    payment_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    payment_method = db.Column(db.String(255), nullable=False)
    payment_ref = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float(), nullable=False)

     # foreign keys
    fk_guest_id = db.Column(db.Integer(), db.ForeignKey("guest.guest_id"))
    fk_customer_id = db.Column(db.Integer(), db.ForeignKey("customer.customer_id"))

    #relationship
    customer_payment = db.relationship('Customer', back_populates ='payment_customer')
    guest_payment = db.relationship('Guest', back_populates ='payment_guest')


class Subscribers(db.Model):
    subscribers_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    subscribers_email = db.Column(db.String(255), nullable=False)