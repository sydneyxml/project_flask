from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:095628@localhost/BMI_collector"

db = SQLAlchemy(app)

class Data(db.Model):
  __tablename__ = "data"
  id = db.Column(db.Integer, primary_key=True)
  email_ = db.Column(db.String(100), unique=True)
  height_ = db.Column(db.Integer)
  weight_ = db.Column(db.Integer)
  bmi_ = db.Column(db.Float)

  def __init__(self, email_, height_, weight_, bmi_):
      self.email_ = email_
      self.height_ = height_
      self.weight_ = weight_
      self.bmi_ = bmi_

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
  if request.method == "POST":
    email = request.form["email_name"]
    height = request.form["height_name"]
    weight = request.form["weight_name"]
    bmi = "{:.2f}".format(eval(weight)/(eval(height)/100)**2)
    
    if db.session.query(Data).filter(Data.email_ == email).count() == 0:
      data = Data(email, height, weight, bmi)
      db.session.add(data)
      db.session.commit()
      average_bmi = db.session.query(func.avg(Data.bmi_)).scalar()
      average_bmi = round(average_bmi, 2)
      count = db.session.query(Data.bmi_).count()
      send_email(email, bmi, average_bmi, count)
      return render_template("success.html")
  return render_template("index.html")


if __name__ == "__main__":
  app.debug = True
  app.run()

