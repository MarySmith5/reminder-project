"""Crud operations"""

from model import db, Customer, Appointment, connect_to_db



# def create_stylist(stylist_name, stylist_contact_num, salon_id):
#     """Create and return a new stylist"""
#     stylist = Stylist(stylist_name=stylist_name, 
#                       stylist_contact_num=stylist_contact_num,
#                       salon_id=salon_id)

#     db.session.add(stylist)
#     db.session.commit()

#     return stylist


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
    return db.session.query(Customer.first_name).filter_by(customer_id).one()
    

def create_appointment(customer_id,  
                       gen_service,
                       specific_service,
                       date,
                       start_time,
                       duration,
                       body_1=None, 
                       when_send1=None, 
                       body_2=None, 
                       when_send2=None,
                       is_canceled=False):

    """Create and return a new appointment"""

    appointment = Appointment(customer_id=customer_id,   
                              gen_service=gen_service,
                              specific_service=specific_service,
                              date=date,
                              start_time=start_time,
                              duration=duration,
                              body_1=body_1, 
                              when_send1=when_send1, 
                              body_2=body_2,
                              when_send2=when_send2,
                              is_canceled=is_canceled)
    db.session.add(appointment)
    db.session.commit()

    return appointment


def get_appointment(customer_id):
    """Finds and returns a specific appointment by customer and date"""

    return Appointment.query.filter_by(customer_id='customer_id').all()


# def create_reminder(appt_id, 
#                     body_1, 
#                     when_send1, 
#                     body_2, 
#                     when_send2, 
#                     is_canceled=False):

#     """Create and return reminder"""
#     reminder = Reminder(appt_id=appt_id, 
#                     body_1=body_1, 
#                     when_send1=when_send1, 
#                     body_2=body_2, 
#                     when_send2=when_send2, 
#                     is_canceled=is_canceled)

#     db.session.add(reminder)
#     db.session.commit()

#     return reminder




if __name__ == '__main__':
    from server import app
    connect_to_db(app)