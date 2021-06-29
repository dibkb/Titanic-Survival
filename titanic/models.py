from datetime import datetime
from titanic import db


class User(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   name = db.Column(db.String(120),unique = False, nullable = False)
   date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   score = db.Column(db.Float(6),unique = False, nullable = False)

   def __repr__(self):
       return f"User('{self.name}','{self.score}')"
   
