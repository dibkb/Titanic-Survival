  
from flask import render_template, url_for, redirect,request
from titanic import app , db
from titanic.forms import UserForm
from titanic.models import User
import pandas as pd
import pickle

model = pickle.load(open('titanic.pkl', 'rb'))
ohe_enc = pickle.load(open('ohe_enc.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))


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

      user = User(name = form.name.data,score = prob)
      db.session.add(user)
      db.session.commit()
      
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

