from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors
import re
import mysql.connector
from PIL import Image
from io import BytesIO
from flask import send_from_directory

app = Flask(__name__)
app.secret_key=os.urandom(24)#to ensure session expiring
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='riddhi@2108',
    database="WEBSITE"
)

cursor=conn.cursor()
@app.route('/')
def login():
    message = session.pop('message', None)
    return render_template('loginpage.html',message=message)


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/home')
def home():
    if 'user_id' in session:
        username=session['username']
        message=f"hello,{username}"
        logged_in=True
        return render_template('home.html',message=message,logged_in=logged_in)
    else:
        session['message']='please login!'
        return redirect('/')
# @app.route('/products')
# def about():
#     return render_template('products.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

# @app.route('/products')
# def products():
#     return render_template('products.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/sell')
def sell():
    #user=session.pop()
    
    if 'user_id' in session:
        username=session['username']
        message=f"hello,{username}"
        logged_in=True
        if session['user_type']=='seller':
            return render_template('sell.html',message=message,logged_in=logged_in)
        else:
            message=f"you are a buyer, login as seller to sell products!"
            return render_template('home.html',message=message,logged_in=logged_in)
    else:
        session['message']='please login!'
        return redirect('/')


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
def login_validation():
    message = ''
    email = request.form.get('EmailId')
    password = request.form.get('Pass')
    role=request.form.get("role")
    
    # Check in the Customer table
    if role=='buyer':
        cursor.execute("SELECT * FROM Customer WHERE EmailId = %s AND CustPass = %s", (email, password))
        customer = cursor.fetchall()
        if customer : 
            session['user_id'] = customer[0][0]
            session['username'] = customer[0][5]  # You may adjust this index if needed
            session['user_type'] = 'customer'  # Add a user type
            session['message'] = 'Logged in successfully as a customer'
            return redirect('/home')
        else:
            session['message'] = 'Invalid credentials'
            return redirect('/')
    else :
    # Check in the Seller table
        cursor.execute("SELECT * FROM Sellerretailer WHERE EmailId = %s AND SellPass = %s", (email, password))
        seller = cursor.fetchall()
        if seller:
        # If the user is found in the Seller table
            session['user_id'] = seller[0][0]
            session['username'] = seller[0][5]  # Adjust this index accordingly
            session['user_type'] = 'seller'  # Add a user type
            session['message'] = 'Logged in successfully as a seller'
            return redirect('/home')
        else:
            session['message'] = 'Invalid credentials'
            return redirect('/')
    
@app.route('/add_user',methods=['POST'])
def add_user():
    email=request.form.get('email_reg')
    password=request.form.get('password_reg')
    confirmPassword=request.form.get('confirmPassword')
    phone=request.form.get('phone_reg')
    role = request.form.get('role') #implement logic that a person can be both buyer and seller hence can use same email for both accounts,right now it searches only for an email in the customer table
    if role == "buyer":
        print("haha")
        cursor.execute("SELECT * FROM Customer WHERE EmailId LIKE '{}'".format(email))
        account = cursor.fetchone()
        if account:
            session['message'] = 'Account already exists !'
            return redirect('/') #or go to login page if this is not working
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            session['message'] = 'Invalid email address !'
            return redirect('/')
        elif password!=confirmPassword:
            session['message']="password and confirm password do not match"
            return redirect('/')
        else:
            cursor.execute("INSERT INTO Customer (FirstName, LastName, Age, Gender, EmailId, Contact, ShippingAddress, Pincode_Shipping, City_Shipping, BillingAddress, Pincode_Billing, City_Billing, CustPass) VALUES (NULL, NULL, NULL, NULL,'{}','{}',NULL, NULL, NULL, NULL, NULL, NULL,'{}')".format(email,phone,password))
            conn.commit()
            session['message']= 'You have successfully registered as a buyer !'
    else:
        cursor.execute("SELECT * FROM SellerRetailer WHERE EmailId LIKE '{}'".format(email))
        account = cursor.fetchone()
        if account:
            session['message'] = 'Account already exists !'
            return redirect('/') #or go to login page if this is not working
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            session['message'] = 'Invalid email address !'
            return redirect('/')
        elif password!=confirmPassword:
            session['message']="password and confirm password do not match"
            return redirect('/')
        else:
            cursor.execute("INSERT INTO SellerRetailer (FirstName, LastName, Age, Gender, EmailId, Contact,PaymentInfo,BillingAddress,SellPass) VALUES (NULL, NULL, NULL, NULL,'{}','{}', NULL, NULL,'{}')".format(email,phone,password))
            conn.commit()
            session['message']= 'You have successfully registered as a seller !'
    return redirect('/')
@app.route('/add_product',methods=["POST"])        
def add_product():
    if 'user_id' in session and session['user_type']=='seller':
        title=request.form.get('Title')
        description=request.form.get('description')
        price=request.form.get('price')
        image=request.files.get('image')
        sellerid=session['user_id']
        if image.filename != '':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            print(filepath)
            filename="../uploads/"+image.filename
            print(filename)
            
            image.save(filepath)
            #print(filename)
            
        cursor.execute("INSERT INTO Product( ProductId,Price,Category,Description,ProductImages,QuantityAvailable,EstimatedDeliveryTime,SellerId,product_name) VALUES (NULL,'{}',NULL,'{}','{}',NULL,NULL,'{}','{}')".format(price,description,filename,sellerid,title))
        conn.commit()
        session['message']= 'You have successfully added product !'
        return redirect('/home')
    else:
        return redirect('/home')  

@app.route('/products')
def products():
    # Fetch product data from the database
    cursor.execute("SELECT ProductId, Price, Description, ProductImages, product_name FROM Product")
    products = cursor.fetchall()
    print(products[0])

    return render_template('products.html', products=products)



            
if __name__ == '__main__':
    app.run(debug=True)

