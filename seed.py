"""Seed database with sample data from CSV Files."""

from app import db
from models import User, Movie, List

db.drop_all()
db.create_all()

dof = User.signup(username="dof", password="dofdof")

m1 = Movie(id="tt11057302")

db.session.add_all([dof, m1])
db.session.commit()

l1 = List(user_id=1, movie_id="tt11057302")

db.session.add(l1)
db.session.commit()
