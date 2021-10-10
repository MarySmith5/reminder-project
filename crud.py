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


def create_appointment()


