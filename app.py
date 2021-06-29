from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, redirect,request
from forms import UserForm
from datetime import datetime
import pandas as pd
import pickle
import os
import re


model = pickle.load(open('pickle/titanic.pkl', 'rb'))
ohe_enc = pickle.load(open('pickle/ohe_enc.pkl', 'rb'))
scaler = pickle.load(open('pickle/scaler.pkl', 'rb'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u23t4y2g4hj1ygh4i4y234234bkj3juy43uyy4d'

#comment this part in development
uri = os.getenv("DATABASE_URL")  
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)



ENV = 'production'

if ENV == 'dev':
   app.debug = True
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
else:
   app.debug = False
   app.config['SQLALCHEMY_DATABASE_URI'] = uri  

db = SQLAlchemy(app)

#Database model
class User(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   name = db.Column(db.String(120),unique = False, nullable = False)
   date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   score = db.Column(db.Float(6),unique = False, nullable = False)

   def __repr__(self):
       return f"User('{self.name}','{self.score}')"



#define routes
@app.route('/')
@app.route('/home')
def home():
   return render_template('index.html')



@app.route('/form',methods = ['GET','POST'])
def form():
   form = UserForm()
   if form.validate_on_submit():
      input_dict = {
         "Name_prefix" : [request.form['Name_prefix']],
         "Embarked": [request.form['Embarked']],
         "Fare":form.fare.data,
         "Parch":request.form['Parch'],
         "SibSp":request.form['SibSp'],
         "Age":form.age.data,
         "Sex":[request.form['Sex']],
         "Pclass":request.form['Pclass']
      }

      input_df = pd.DataFrame.from_dict(input_dict)
      input_df = input_df.sort_index(axis = 1)

      input_df = ohe_enc.transform(input_df)
      prob = model.predict_proba(scaler.transform(input_df))[0][1]
      prob = round((prob * 100),2)
      
      #add to database only if the user gives concent
      try:
         concent = int(request.form['concent'])
      except:
         concent = 0
      print(concent)
      if concent == 1:
         user = User(name = form.name.data,score = prob)
         db.session.add(user)
         db.session.commit()
         print('success')
      
      if prob >= 50:
         return render_template('result.html',prob = prob,name = form.name.data)
            
      else:
         return render_template('resultFail.html',prob = prob,name = form.name.data)   

   return render_template('form.html',form = form)

@app.route('/form-mobile',methods = ['GET','POST'])
def formMobile():
   form = UserForm()
   if form.validate_on_submit():
      input_dict = {
         "Name_prefix" : [request.form['Name_prefix']],
         "Embarked": [request.form['Embarked']],
         "Fare":form.fare.data,
         "Parch":request.form['Parch'],
         "SibSp":request.form['SibSp'],
         "Age":form.age.data,
         "Sex":[request.form['Sex']],
         "Pclass":request.form['Pclass']
      }

      input_df = pd.DataFrame.from_dict(input_dict)
      input_df = input_df.sort_index(axis = 1)

      input_df = ohe_enc.transform(input_df)
      prob = model.predict_proba(scaler.transform(input_df))[0][1]
      prob = round((prob * 100),2)
      try:
         concent = int(request.form['concent'])
      except:
         concent = 0
      print(concent)
      if concent == 1:
         user = User(name = form.name.data,score = prob)
         db.session.add(user)
         db.session.commit()
         print('success')
      

      if prob >= 50:
         return render_template('result.html',prob = prob,name = form.name.data)
            
      else:
         return render_template('resultFail.html',prob = prob,name = form.name.data)   

   return render_template('formMobileCopy.html',form = form) 


@app.route('/statistics')
def statisics():
   return render_template('statistics.html')

@app.route('/leaderboard')
def leaderboard():
   users = User.query.order_by(User.score).all()[::-1]
   return render_template('leaderboard.html',users = users)             








if __name__ == '__main__':
    app.run()