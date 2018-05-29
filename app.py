from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime as dt

app = Flask(__name__) 
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/simplebook_db'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ywaiwgvvfqdhki:1b40eb6191012a19ac3f59ea91d3b215225cf560a1e39367ec51888d3fd13740@ec2-75-101-142-91.compute-1.amazonaws.com:5432/d6hd5a4dgq8e78?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50))
	last_name = db.Column(db.String(50))
	email = db.Column(db.String(120), unique=True)
	phone_number = db.Column(db.String(20), unique=True)
	address = db.Column(db.String(255))
	gender = db.Column(db.Integer)
	dob = db.Column(db.Date)
	timestamp = db.Column(db.Date)

	def __init__(self, first_name, last_name, email, phone_number, address, gender, dob, timestamp):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.phone_number = phone_number
		self.address = address
		self.gender = gender
		self.dob = dob
		self.timestamp = timestamp


@app.route('/')
def home():
	return render_template("home.html", text='Please fill all fields', alert_style='alert alert-success')

@app.route("/my_algorithms", methods=['POST', 'GET'])
def my_algorithms():
	if request.method == 'POST':
		my_string = request.form["my_string"]
		if my_string != '':

			def duplicate_string(my_string):
			    my_dict = {}
			    string_status = 'All Unique'
			    for c in my_string:
			        if c in my_dict:
			            my_dict[c] = my_dict[c]+1
			            string_status = 'Duplicate Found'
			        else:
			            my_dict[c] = 1
			    
			    # for k,v in my_dict.items():
			    #     if v > 1:
			    #         print(k,v)
			    return string_status

			string_check = my_string.replace(" ","")
			string_check = duplicate_string(string_check)
		else:
			string_check = 'No String Sent'

		factorize = int(request.form["factorize"])
		if factorize != '':
			prime_factor = []
			def prime_factorization(my_number, prime_factors):
			    
			    while my_number % 2 == 0:
			        prime_factors.append(2)
			        my_number = int(my_number/2)
			        # factorization(the_number,prime_factors)
			    for i in range(3, my_number+1,2):
			        while my_number % i == 0:
			            prime_factors.append(i)
			            my_number = int(my_number/i)
			            # factorization(the_number,prime_factors)
			    return(prime_factors)

			factorization = prime_factorization(factorize, prime_factor)
		else:
			factorization = 'No Number Entered'
		return render_template("my_algorithms.html", string_check=string_check, factorization=factorization )
	else:
		return render_template("my_algorithms.html", string_check='', factorization='')

@app.route("/customer")
def customers():
	users = db.session.query(Data).order_by(Data.id).all()
	users_count = db.session.query(Data).order_by(Data.id).count()
	return render_template("customers.html", users=users, users_count=users_count)

@app.route("/view_customer/<id>")
def view_customer(id):
	# customer_id = request.args.get('id')
	customer = db.session.query(Data).filter(Data.id == id).first()
	print(customer.first_name)
	return render_template("view_customer.html", customer=customer)

@app.route("/success", methods=['POST'])
def success():
	if request.method == 'POST':
		first_name = request.form["first_name"]
		last_name = request.form["last_name"]
		email = request.form["email"]
		phone_number = request.form["phone_number"]
		address = request.form["address"]
		dob = request.form["dob"]
		gender = request.form["gender"]
		timestamp = dt.now()
		# print(first_name,last_name,phone_number,address, email,dob, timestamp)
		if db.session.query(Data).filter(Data.email == email).count()  > 0:
			return render_template("home.html", text="Sorry, Seems that Email Address already Exists", alert_style='alert alert-danger')
		elif db.session.query(Data).filter(Data.phone_number == phone_number).count() > 0:
			return render_template("home.html", text="Sorry, Seems that Phone Number already Exists", alert_style='alert alert-danger')
		else:
			user = Data(first_name, last_name, email, phone_number, address, gender, dob, timestamp)
			db.session.add(user)
			db.session.commit()
			return render_template("success.html")

		

if __name__ == '__main__':
	app.debug = True
	app.run()