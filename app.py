# from flask import Flask, render_template,request

# from flask_wtf import Form
# from wtforms import TextField,validators,TextAreaField,StringField,SubmitField

# class ReviewForm(Form):
#     name = TextField("Username",[validators.DataRequired("Please enter your name.")])
#     product = TextField("Product Name",[validators.DataRequired("Please enter the product name.")])
#     review = TextField("Review",[validators.DataRequired("Please enter the review for the product.")])
#     submit = TextField("Submit")
#     # product=TextField('ProductName',validators[validators.DataRequired()])
#     # review=TextField('Review',validators[Validators.DataRequired()])
#     # submit=SubmitField('Submit')

# @app.route('/', methods= ['GET','POST'])
# def Review():
#     form= ReviewForm()
#     if request.method == 'POST':
#         pass
#     else:
#         render_template('index.html',form=form)



# if __name__ == '__main__':
#    app.run(debug = True)

from flask import Flask, render_template, request,flash,redirect, url_for
from io import TextIOWrapper
import csv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY']='helloworld'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    product = db.Column(db.String(80))
    review = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    


    def __repr__(self):
       return '<User %r>' % self.id
      #  return "<User: {}>".format(self.username)


from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField

from wtforms import validators, ValidationError

class ReviewForm(Form):
   name = TextField("UserName",[validators.DataRequired("Please enter your name.")])
   product = TextField("Product Name",[validators.DataRequired("Please enter the product name")])
   review = TextAreaField("Review",[validators.DataRequired("Please enter the review")])

   submit = SubmitField("Submit")






@app.route('/', methods = ['GET', 'POST'])
def Review():
   form = ReviewForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('index.html', form = form)
      else:
         nm = form.name.data
         prod = form.product.data
         rview = form.review.data

         entry=User(username=nm,product=prod,review=rview)
         db.session.add(entry)
         db.session.commit()
         return redirect('/')


         #return "Thankyou for your response"
         # csv_file = request.files['file']
         # csv_file = TextIOWrapper(csv_file, encoding='utf-8')
         # csv_reader = csv.reader(csv_file, delimiter=',')
         # for row in csv_reader:
         #    user = User(username=row[0], product=row[1],review=row[2])
         #    db.session.add(user)
         #    db.session.commit()
         # return redirect(url_for('upload_csv'))
   elif request.method == 'GET':
      # reviews = User.query.order_by(User.username).all()
      reviews=User.query.order_by(User.date_created).all()
      return render_template('index.html', form = form,reviews=reviews)

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)