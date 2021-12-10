"""Crud operations"""

from model import db, Customer, Appointment, connect_to_db
from datetime import datetime, timezone, timedelta
import arrow
import time
import tasks


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
                       date,
                       time,
                       timezone,
                       duration,
                       specific_service="No notes",
                       body=None,
                       body_1=None, 
                       body_2=None, 
                       is_canceled=False,
                       sent_1=False,
                       sent_2=False
                       ):

    """Create and return a new appointment"""

    appointment = Appointment(customer_id=customer_id,   
                              gen_service=gen_service,
                              date_time=date_time,
                              date=date,
                              time=time,
                              timezone=timezone,
                              duration=duration,
                              specific_service=specific_service,
                              body=body,
                              body_1=body_1,  
                              body_2=body_2,
                              is_canceled=is_canceled,
                              sent_1=sent_1,
                              sent_2=sent_2
                              )

    appointment.date_time = arrow.get(appointment.date_time, appointment.timezone).to('utc').naive
    db.session.add(appointment)
    db.session.commit()
    
    tasks.send_sms_reminder_now(appointment.appoint_id)
    now = datetime.utcnow().date()
    
    print(f"NOW DATE: {now}")
    print(f"APPOINTMENT DATE: {appointment.date}")
    if appointment.is_canceled == False:
        if appointment.date != now:
            tasks.send_sms_reminder1.apply_async(
                        args=[appointment.appoint_id], eta=appointment.get_remind_time1()
                    )
        tasks.send_sms_reminder2.apply_async(
                    args=[appointment.appoint_id], eta=appointment.get_remind_time2()
                )

    
    return appointment


# def get_remind1():
#     now = datetime.today()+timedelta(days=-1)
#     date=datetime.date(now)
#     print(date)
#     return Appointment.query.filter_by(date=date, is_canceled=False).all()


# def get_remind2():
#     now = datetime.today()
#     date = datetime.date(now)
#     print(date)
#     return Appointment.query.filter_by(date=date, is_canceled=False).all()


def get_appointment(customer_id):
    """Finds and returns appointments by customer"""
    
    return Appointment.query.filter_by(customer_id=customer_id).order_by('date').all()


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


# def mark_as_sent(appoint_id, which_send):
#     """Updates reminder-sent status"""

#     r = Appointment.query.filter_by(appoint_id=appoint_id).one()
#     r.which_send = True
#     db.session.commit()
#     return r



if __name__ == '__main__':
    from server import app
    connect_to_db(app)