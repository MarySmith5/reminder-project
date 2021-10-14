"""Crud operations"""

from model import db, Salon, Stylist, Customer, Appointment, Reminder, connect_to_db



def create_salon(salon_name, salon_email, password):
    """Create and return a new user/salon"""
    user = Salon(salon_name=salon_name, salon_email=salon_email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_salon_by_email(email):

    return Salon.query.filter_by(salon_email == email).first()


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


def get_cust_id(first_name, last_name):
    """Find a customer's id by name"""

    return Customer.query.filter_by(first_name=first_name, last_name=last_name).all()


def create_appointment(customer, 
                       stylist, 
                       gen_service,
                       specific_service,
                       date,
                       start_time,
                       end_time,
                       is_canceled=False):

    """Create and return a new appointment"""

    appointment = Appointment(customer=customer,  
                              stylist=stylist, 
                              gen_service=gen_service,
                              specific_service=specific_service,
                              date=date,
                              start_time=start_time,
                              end_time=end_time,
                              is_canceled=is_canceled)
    db.session.add(appointment)
    db.session.commit()

    return appointment


def get_appointment(customer):
    """Finds and returns a specific appointment by customer and date"""

    return Appointment.query.filter_by(cust_id='customer').all()


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




if __name__ == '__main__':
    from server import app
    connect_to_db(app)