"""Models for reminder app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Salon(db.Model):
    """An app user that holds an account"""

    __tablename__ = "salons"

    salon_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    salon_email = db.Column(db.String(50), nullable=False)
    salon_name = db.Column(db.String(50))
    password = db.Column(db.String(25), nullable=False)

    employees = db.relationship("Stylist", back_populates='salon')

class Stylist(db.Model):
    """A person serving appointments"""

    __tablename__ = "stylists"

    stylist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stylist_name = db.Column(db.String(30), nullable=False)
    stylist_contact_num = db.Column(db.Integer, nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salons.salon_id'))

    salon = db.relationship('Salon', back_populates='employees')
    appts = db.relationship('Appointment', back_populates='my_stylist')

    def __repr__(self):
        """Show info about a stylist"""
        return f"<Stylist id={self.stylist_id}, name={self.stylist_name}, contact={self.stylist_contact_num}>"


class Customer(db.Model):
    """A person receiving a service"""

    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    text_num = db.Column(db.Integer)
    calls_only_num = db.Column(db.Integer)
    customer_email = db.Column(db.String(50))

    appts = db.relationship('Appointment', back_populates='my_customer')

    def __repr__(self):
        """Show info about a customer"""
        return f"<Customer id={self.customer_id}, first name={self.first_name}, text={self.text_num}, email={self.customer_email}>"


class Appointment(db.Model):
    """A scheduled event"""

    __tablename__ = "appointments"

    appoint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylists.stylist_id'))
    gen_service = db.Column(db.String(25), nullable=False)
    specific_service = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    is_canceled = db.Column(db.Boolean)

    my_stylist = db.relationship('Stylist', back_populates='appts')
    my_customer = db.relationship('Customer', back_populates='appts')
    remind = db.relationship('Reminder', back_populates='appt')

    def __repr__(self):
        """Show info about an appointment"""
        return f"<Appointment id={self.appoint_id}, service={self.gen_service}, date={self.date}>"


class Reminder(db.Model):
    """A customized message to remind a customer of an appointment"""

    __tablename__ = 'reminders'

    remind_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appt_id = db.Column(db.Integer, db.ForeignKey('appointments.appoint_id'), nullable=False)
    body_1 = db.Column(db.Text)
    when_send1 = db.Column(db.DateTime)
    body_2 = db.Column(db.Text)
    when_send2 = db.Column(db.DateTime)
    is_canceled = db.Column(db.Boolean)

    appt = db.relationship('Appointment', back_populates='remind')

    def __repr__(self):
        """Shows a reminder"""
        return f"<Reminder id={self.remind_id}, send={self.when_send1}>"


def connect_to_db(flask_app, db_uri="postgresql:///reminders", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)












