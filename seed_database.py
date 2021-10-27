import os
import crud
import model
import server
from datetime import datetime

os.system('dropdb reminders')
os.system('createdb reminders')

model.connect_to_db(server.app)
model.db.create_all()


crud.create_customer('Customer', 'Try', '5551234567', '5551234568', 'customer@test.test')
crud.create_customer('Another', 'Customer', '2385554444', None, None)
crud.create_customer('Jane', 'Doe', '5678994444', None, None)
crud.create_customer('Mary', 'Smith', '3333333333', None, None)
crud.create_customer('Mary', 'Smith', '2222222222', None, None)

crud.create_appointment(1, 'hair', 'woman cut', datetime(2021, 11, 2, 16, 30), "0:45", "HI", datetime(2021, 11, 1, 16, 30), "hello", datetime(2021, 11, 2, 14, 30), False)
crud.create_appointment(2, 'hair', 'man cut', datetime(2021, 11, 3, 16, 30), "0:30", "HI", datetime(2021, 11, 2, 16, 30), "hello", datetime(2021, 11, 3, 14, 30), False)
crud.create_appointment(3, 'hair', 'highlights', datetime(2021, 11, 4, 16, 30), "0:45", "HI", datetime(2021, 11, 3, 16, 30), "hello", datetime(2021, 11, 4, 14, 30), False)
crud.create_appointment(3, 'hair', 'wax eyebrows', datetime(2021, 11, 5, 16, 30), "0:30", "HI", datetime(2021, 11, 4, 16, 30), "hello", datetime(2021, 11, 5, 14, 30), False)
crud.create_appointment(4, 'hair', 'woman cut', datetime(2021, 11, 6, 16, 30), "0:45", "HI", datetime(2021, 11, 5, 16, 30), "hello", datetime(2021, 11, 6, 14, 30), False)
crud.create_appointment(4, 'hair', 'color', datetime(2021, 12, 3, 16, 30), "0:30", "HI", datetime(2021, 12, 2, 16, 30), "hello", datetime(2021, 12, 3, 14, 30), False)
crud.create_appointment(4, 'hair', 'highlights', datetime(2021, 11, 15, 16, 30), "0:45", "HI", datetime(2021, 11, 14, 16, 30), "hello", datetime(2021, 11, 15, 14, 30), False)
crud.create_appointment(5, 'nail', 'full set', datetime(2021, 11, 7, 12, 30), "0:30", "HI", datetime(2021, 11, 6, 12, 30), "hello", datetime(2021, 11, 7, 10, 30), False)




