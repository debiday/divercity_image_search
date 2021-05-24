"""Load user data into database."""

from model import User, Collection, Picture, connect_to_db, db
from server import app

import os
import json
from random import choice, randint
from datetime import datetime

import crud

os.system('dropdb images')
os.system('createdb images')

connect_to_db(app)
db.create_all()

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
