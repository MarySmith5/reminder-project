"""Crud operations"""

from model import db, Salon, Stylist, Customer, Appointment, Reminder, connect_to_db

def create_salon(salon_name, salon_email, password):
    """Create and return a new user/salon"""
    user = Salon(salon_name=salon_name, salon_email=salon_email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def create_stylist(stylist_name, stylist_contact_num, salon):
    """Create and return a new stylist"""
    stylist = Stylist(stylist_name=stylist_name, 
                      stylist_contact_num=stylist_contact_num,
                      salon=salon)

    db.session.add(stylist)
    db.session.commit()

    return stylist


def create_customer(first_name, 
                   last_name, 
                   text_num, 
                   calls_only_num, 
                   customer_email):
    """Create and return a new customer"""

    customer = Customer(first_name=first_name, 
                        last_name=last_name, 
                        text_num=text_num, 
                        calls_only_num=calls_only_num, 
                        customer_email=customer_email)

    db.session.add(customer)
    db.session.commit()

    return customer


def create_appointment(customer, 
                       stylist, 
                       gen_service,
                       specific_service,
                       date,
                       time,
                       duration,
                       is_canceled=False):

    """Create and return a new appointment"""

    appointment = Appointment(customer=customer,  
                              stylist=stylist, 
                              gen_service=gen_service,
                              specific_service=specific_service,
                              date=date,
                              time=time,
                              duration=duration,
                              is_canceled=is_canceled)
    db.session.add(appointment)
    db.session.commit()

    return appointment


def create_reminder(appt, 
                    body_1, 
                    when_send1, 
                    body_2, 
                    when_send2, 
                    is_canceled=False):

    """Create and return reminder"""
    reminder = Reminder(appt=appt, 
                    body_1=body_1, 
                    when_send1=when_send1, 
                    body_2=body_2, 
                    when_send2=when_send2, 
                    is_canceled=is_canceled)

    db.session.add(reminder)
    db.session.commit()

    return reminder
    