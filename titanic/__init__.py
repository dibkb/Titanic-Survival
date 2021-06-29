from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u23t4y2g4hj1ygh4i4y234234bkj3juy43uyy4d'

ENV = 'dev'
if ENV == 'dev':
   app.debug = True
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
else:
   app.debug = False
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://oqhhokcvvfvjla:34ef48c27121496d5caf0e3e96e4fe500a587d172f90579665db47ee75c1a157@ec2-52-5-247-46.compute-1.amazonaws.com:5432/duf1v9ao1cpb6ws.com:5432/duf1v9ao1cpb6'  

db = SQLAlchemy(app)



from titanic import routes