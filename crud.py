"""Crud operations"""

from model import db, Customer, Appointment, connect_to_db
import tasks
from datetime import datetime, timezone, timedelta
import arrow
import time


def create_customer(first_name, 
                   last_name, 
                   text_num=None, 
                   landline=None, 
                   email=None):
    """Create and return a new customer"""

    customer = Customer(first_name=first_name, 
                        last_name=last_name, 
                        text_num=text_num, 
                        landline=landline, 
                        email=email)

    db.session.add(customer)
    db.session.commit()

    return customer


def get_cust(first_name, last_name):
    """Find a customer by name"""
    return Customer.query.filter_by(first_name=first_name, last_name=last_name).all()


def get_cust_id(first_name, last_name):
    """Find a customer's id by first and last name"""
    return db.session.query(Customer.customer_id).filter_by(first_name=first_name, last_name=last_name).all()
    

def get_cust_fname(customer_id):
    """Find a customer's first name by id"""
    q = Customer.query.filter_by(customer_id=customer_id).one()
    return q.first_name

def check_existing_cust(first_name, last_name, text_num):
    """Check to see if a customer already exists"""
    return Customer.query.filter_by(first_name = first_name, last_name = last_name, text_num = text_num).first()  


def create_appointment(customer_id,  
                       gen_service,
                       date_time,
                       duration,
                       specific_service="No notes",
                       body_1=None, 
                       body_2=None, 
                       is_canceled=False,
                       reminder1_sent=False,
                       reminder2_sent=False):

    """Create and return a new appointment"""

    appointment = Appointment(customer_id=customer_id,   
                              gen_service=gen_service,
                              specific_service=specific_service,
                              date_time=date_time,
                              duration=duration,
                              body_1=body_1,  
                              body_2=body_2,
                              is_canceled=is_canceled,
                              reminder1_sent=reminder1_sent,
                              reminder2_sent=reminder2_sent)
    db.session.add(appointment)
    db.session.commit()

    return appointment


def get_appointment(customer_id):
    """Finds and returns appointments by customer"""
    return Appointment.query.filter_by(customer_id=customer_id).all()


def get_appt_by_id(appoint_id):
    """Finds and returns an appoinment by its id"""
    return Appointment.query.filter_by(appoint_id=appoint_id).one()


def get_cust_by_appt_id(appoint_id):
    """Finds and returns a customer id by an appointment id."""
    c = Appointment.query.filter_by(appoint_id=appoint_id).one()
    return c.my_customer.customer_id


def cancel_appt(appoint_id):
    """Marks appointment as canceled"""
    a = Appointment.query.filter_by(appoint_id=appoint_id).one()
    a.is_canceled = True
    db.session.commit()
    return a


def get_appt_remind2():
    today = datetime.date.now()
    appts_to_remind2 = Appointment.query.filter(Appointment.date_time == today, Appointment.my_customer.text_num!=None, Appointment.is_canceled==False, Appointment.reminder2_sent==False).all()
    return appts_to_remind2


def get_appt_remind1():
    tomorrow = datetime.date.now() + timedelta(days=1)
    appts_to_remind1 = Appointment.query.filter(Appointment.date_time == tomorrow, Appointment.my_customer.text_num!=None, Appointment.is_canceled==False, Appointment.reminder1_sent==False).all()
    return appts_to_remind1



if __name__ == '__main__':
    from server import app
    connect_to_db(app)