"""Models for reminder app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stylist(db.Model):
    """A person serving appointments"""

    __tablename__ = "stylists"

    stylist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stylist_name = db.Column(db.String(30), nullable=False)
    stylist_contact_num = db.Column(db.Integer, nullable=False)

    apmnts = db.relationship('Appointment', back_populates='my_stylist')

    def __repr__(self):
        """Show info about a stylist"""
        return f"<Stylist id={self.stylist_id}, name={self.stylist_name}, contact={self.stylist_contact_num}>"


