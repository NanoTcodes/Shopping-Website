from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors
import re
import mysql.connector

app = Flask(__name__)
app.secret_key=os.urandom(24)#to ensure session expiring
conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Shaurya3477',
    database="WEBSITE"
)
cursor=conn.cursor()
@app.route('/')
def home():
    message=session.pop('message',None)
    return render_template('home.html',message=message)

@app.route('/products')
def about():
    return render_template('products.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/sell')
def sell():
    #user=session.pop()
    
    return render_template('sell.html')

@app.route('/login')
def login():
    message = session.pop('message', None)
    return render_template('loginpage.html',message=message)
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
@app.route('/login_validation',methods=['POST'])
def login_validation():#add logic for logging into both seller and buyer accounts
    message=''
    email=request.form.get('EmailId')
    password=request.form.get('CustPass')
    cursor.execute("SELECT * FROM Customer where EmailId LIKE '{}' AND CustPass LIKE '{}' ".format(email,password))
    user=cursor.fetchall() #data retruned will be inside a tuple,empty tuple will be returned if user credentials dont match
    if len(user)>0:
        session['user_id']=user[0][0]
        session['message']='logged in succesfully'
        return redirect('/')
    else:
        session['message'] = 'invalid credentials'
        return redirect('/login')
@app.route('/add_user',methods=['POST'])
def add_user():
    email=request.form.get('email_reg')
    password=request.form.get('password_reg')
    confirmPassword=request.form.get('confirmPassword')
    phone=request.form.get('phone_reg')
    role = request.form.get('role') #implement logic that a person can be both buyer and seller hence can use same email for both accounts,right now it searches only for an email in the customer table
    cursor.execute("SELECT * FROM Customer WHERE EmailId LIKE '{}'".format(email))
    account = cursor.fetchone()
    if account:
        session['message'] = 'Account already exists !'
        return redirect('/login') #or go to login page if this is not working
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        session['message'] = 'Invalid email address !'
        return redirect('/login')
    elif password!=confirmPassword:
        session['message']="password and confirm password do not match"
        return redirect('/login')
    else:
            if role=="buyer":
                cursor.execute("INSERT INTO Customer (FirstName, LastName, Age, Gender, EmailId, Contact, ShippingAddress, Pincode_Shipping, City_Shipping, BillingAddress, Pincode_Billing, City_Billing, CustPass) VALUES (NULL, NULL, NULL, NULL,'{}','{}',NULL, NULL, NULL, NULL, NULL, NULL,'{}')".format(email,phone,password))
                conn.commit()
                session['message']= 'You have successfully registered as a buyer !'
            else:
                cursor.execute("INSERT INTO SellerRetailer (FirstName, LastName, Age, Gender, EmailId, Contact,PaymentInfo,BillingAddress,SellPass) VALUES (NULL, NULL, NULL, NULL,'{}','{}', NULL, NULL,'{}')".format(email,phone,password))
                conn.commit()
                session['message']= 'You have successfully registered as a seller !'
            return redirect('/login')

            
if __name__ == '__main__':
    app.run(debug=True)

