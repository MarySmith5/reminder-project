"""Models for reminder app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Customer(db.Model):
    """A person receiving a service"""

    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    text_num = db.Column(db.String(25))
    landline = db.Column(db.String(25))
    email = db.Column(db.String(50))

    appts = db.relationship('Appointment', back_populates='my_customer')

    def __repr__(self):
        """Show info about a customer"""
        return f"<Customer id={self.customer_id}, {self.first_name} {self.last_name}, text={self.text_num}, landline={self.landline}, email={self.email}>"


class Appointment(db.Model):
    """A scheduled event"""

    __tablename__ = "appointments"

    appoint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    gen_service = db.Column(db.String(25), nullable=False)
    specific_service = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, nullable=False)
    #start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Interval)
    body_1 = db.Column(db.Text)
    when_send1 = db.Column(db.DateTime)
    body_2 = db.Column(db.Text)
    when_send2 = db.Column(db.DateTime)
    is_canceled = db.Column(db.Boolean)
    my_customer = db.relationship("Customer", back_populates="appts")
    
    def __repr__(self):
        """Show info about an appointment"""
        return f"< Appointment id={self.appoint_id}, service={self.gen_service}, date_time={self.date_time}, CANCELED={self.is_canceled} >"



def connect_to_db(flask_app, db_uri="postgresql:///reminders", echo=False):
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












