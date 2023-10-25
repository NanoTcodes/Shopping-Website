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
        status="YES"
    else:
        status="NO"
    return render_template('home.html',status=status)
# @app.route('/products')
# def about():
#     return render_template('products.html')

@app.route('/cart')
def cart():
    if 'user_id' in session:
        if session['user_type']=='customer':
            userid = session['user_id']
            cursor.execute("SELECT cart.ProductId, cart.Quantity, cart.Amount, product.product_name, product.ProductImages FROM website.cart INNER JOIN website.product ON cart.ProductId = product.ProductId WHERE cart.CustomerId = %s order by cart.ProductId",(userid,))
            products = cursor.fetchall()
            return render_template('cart.html', products=products)
        else:
            message=f"you are a buyer, login as seller to sell products!"
            return render_template('home.html',message=message)
    else:
        session['message']='please login!'
        return redirect('/')
    
@app.route('/rem_from_cart', methods=['POST'])
def rem_from_cart():
    userid = session['user_id']
    prodid = request.get_json().get('product_id')
    print(prodid)
    cursor.execute("DELETE FROM cart WHERE CustomerId = %s AND ProductId = %s",(userid, prodid))
    conn.commit()
    return redirect(url_for('cart'))   

@app.route('/remall_from_cart')
def remall_from_cart():
    userid = session['user_id']
    cursor.execute("DELETE FROM cart WHERE CustomerId = %s",(userid,))
    conn.commit()
    session['messege']="successfully removed all"
    return render_template('cart.html')

@app.route('/account')
def account():
    if 'user_id' in session:
        CustomerId = session['user_id']

        cursor.execute("SELECT ProductId FROM Wishlist WHERE CustomerId = %s", (CustomerId,))
        wishlist_items = cursor.fetchall()
        return render_template('account.html',wishlist_items=wishlist_items)
    else:
        session['message']='please login!'
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('username',None)
    session.pop('username',None) # Add a user type
    session['message'] = 'Logged out successfully'
    return redirect('/')
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

# @app.route('/products')
# def products():
#     # Fetch product data from the database
#     cursor.execute("SELECT ProductId, Price, Description, ProductImages, product_name FROM Product")
#     products = cursor.fetchall()
#     CustomerId = session['user_id']
#     if 'user_id' in session:
#         status="YES"
#     else:
#         status="NO"
    
#     cursor.execute("SELECT COUNT(*) FROM wishlist WHERE CustomerID = %s AND ProductId = %s", (CustomerId,))
#     already_added = cursor.fetchone()[0] > 0
#     return render_template('products.html', products=products,status=status,already_added=already_added)

@app.route('/products')
def products():
    # Fetch product data from the database
    cursor.execute("SELECT ProductId, Price, Description, ProductImages, product_name FROM Product")
    products = cursor.fetchall()
    
    status = "NO"  # Default status is "NO" if the user is not logged in
    already_added = {}  # Dictionary to store already added status for each product

    if 'user_id' in session:
        status = "YES"
        CustomerId = session['user_id']

        for product in products:
            # Check if the product is already in the user's wishlist
            cursor.execute("SELECT COUNT(*) FROM wishlist WHERE CustomerID = %s AND ProductId = %s", (CustomerId, product[0]))
            already_added[product[0]] = cursor.fetchone()[0] > 0

    return render_template('products.html', products=products, status=status, already_added=already_added)


@app.route('/add_to_wishlist/<int:ProductId>', methods=['POST'])
def add_to_wishlist(ProductId):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    CustomerId = session['user_id']
    cursor = conn.cursor()

    # cur = mysql.get_db().cursor()
    cursor.execute("INSERT INTO Wishlist (CustomerId, ProductId) VALUES (%s, %s)", (CustomerId, ProductId))
    # mysql.get_db().commit()
    conn.commit()
    cursor.close()

    return redirect(url_for('products'))

@app.route('/remove_from_wishlist/<int:ProductId>', methods=['POST'])
def remove_from_wishlist(ProductId):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    CustomerId = session['user_id']
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Wishlist WHERE CustomerId = %s AND ProductId = %s", (CustomerId, ProductId))
    conn.commit()
    cursor.close()

    return redirect(url_for('account'))



# @app.route('/wishlist')
# def wishlist():
    

#     # Fetch product details for wishlist_items if needed

#     return render_template('account.html', wishlist_items=wishlist_items)





            
if __name__ == '__main__':
    app.run(debug=True)

