"""Crud operations"""

from model import db, Stylist, Customer, Appointment, Reminder, connect_to_db

def create_stylist(stylist_name, stylist_contact_num):
    """Create and return a new stylist"""