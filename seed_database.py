import os
import random import choice, randint
import crud
import model
import server

os.system('dropdb reminders')
os.system('createdb reminders')

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    customer = pass