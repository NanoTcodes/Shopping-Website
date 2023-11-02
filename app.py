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

    password='shauryanoob',
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
    session['category']="All"
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

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    
    if 'user_id' in session:
        if session['user_type'] == 'customer':
            user_id = session['user_id']
            
            # Get the product_id and other necessary details from the POST request data.
            product_id = request.form['product_id']
            
            # Retrieve product details from the database
            cursor.execute("SELECT Price FROM product WHERE ProductId = %s", (product_id,))
            product_info = cursor.fetchone()
            
            if product_info:
                price = product_info[0]
                
                # Add the product to the cart with a quantity of 1
                cursor.execute("INSERT INTO cart (CustomerId, ProductId, Quantity, Amount) VALUES (%s, %s, %s, %s)",
                               (user_id, product_id, 1, price))
                
                conn.commit()
                session['message'] = 'Product added to the cart.'
            
            return redirect('/products')
        else:
            session['message'] = 'You need to be a customer to add products to the cart.'
            return redirect('/products')
    else:
        session['message'] = 'Please log in to add products to the cart.'
        return redirect('/')


    
@app.route('/rem_from_cart', methods=['POST'])
def rem_from_cart():
    session['category']="All"
    userid = session['user_id']
    prodid = request.get_json().get('product_id')
    print(prodid)
    cursor.execute("DELETE FROM cart WHERE CustomerId = %s AND ProductId = %s",(userid, prodid))
    conn.commit()
    return redirect(url_for('cart'))   

@app.route('/remall_from_cart')
def remall_from_cart():
    session['category']="All"
    userid = session['user_id']
    cursor.execute("DELETE FROM cart WHERE CustomerId = %s",(userid,))
    conn.commit()
    session['messege']="successfully removed all"
    return render_template('cart.html')

@app.route('/account')
def account():
    session['category']="All"
    if 'user_id' in session:
        #if this id is of seller then dont let it add to wishlist
        CustomerId = session['user_id']
        #print(CustomerId)
        user_type=session['user_type']  #customer and selle#abhi seller ka handle karna baki hai
        if user_type=="customer":
            cursor.execute("select ShippingAddress,Pincode_Shipping,City_Shipping from customer where CustomerId={}".format(CustomerId))
            address=cursor.fetchall()
            cursor.execute("select FirstName,LastName,Age,Gender,EmailId,Contact from customer where CustomerId ={}".format(CustomerId))
            profile_details=cursor.fetchall()

            cursor.execute("SELECT ProductId FROM Wishlist WHERE CustomerId = %s", (CustomerId,))
            wishlist_items = cursor.fetchall()
            return render_template('account.html',wishlist_items=wishlist_items,address=address,profile_details=profile_details)
        else:
            cursor.execute("select BillingAddress from sellerretailer where SellerId={}".format(CustomerId))
            address=cursor.fetchall()
            cursor.execute("select FirstName,LastName,Age,Gender,EmailId,Contact from sellerretailer where SellerId ={}".format(CustomerId))
            profile_details=cursor.fetchall()
            return render_template('account.html',address=address,profile_details=profile_details)
    else:
        session['message']='please login!'
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('username',None)
    session.pop('username',None) # Add a user type
    session.pop('category',None)
    session['message'] = 'Logged out successfully'
    return redirect('/')
@app.route('/sell')
def sell():
    #user=session.pop()
    session['category']="All"
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
            session['username'] = customer[0][1]  # You may adjust this index if needed
            session['user_type'] = 'customer'  # Add a user type
            session['message'] = 'Logged in successfully as a customer'
            session['category']="All"
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
            session['username'] = seller[0][1]  # Adjust this index accordingly
            session['user_type'] = 'seller'  # Add a user type
            session['message'] = 'Logged in successfully as a seller'
            session['category']="All"
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
    first_name=request.form.get('firstName')
    last_name=request.form.get('lastName')
    age=request.form.get('age')
    gender=request.form.get('gender')
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
            cursor.execute("INSERT INTO Customer (FirstName, LastName, Age, Gender, EmailId, Contact, ShippingAddress, Pincode_Shipping, City_Shipping, BillingAddress, Pincode_Billing, City_Billing, CustPass) VALUES ('{}', '{}','{}', '{}','{}','{}',NULL, NULL, NULL, NULL, NULL, NULL,'{}')".format(first_name,last_name,age,gender,email,phone,password))
            conn.commit()
            session['address_type']="buyer"
            session['email']=email
            session['message']= 'You have successfully registered as a buyer !'
            return render_template('buyer.html')
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
            cursor.execute("INSERT INTO SellerRetailer (FirstName, LastName, Age, Gender, EmailId, Contact,PaymentInfo,BillingAddress,SellPass) VALUES ('{}','{}','{}','{}','{}','{}', NULL, NULL,'{}')".format(first_name,last_name,age,gender,email,phone,password))
            conn.commit()
            session["address_type"]="seller"
            #redirect to addres.html of both 
            session['email']=email
            session['message']= 'You have successfully registered as a seller !'
            return render_template('seller.html')
        
@app.route('/add_address',methods=["POST"])
def add_address():
    if session["address_type"]=="buyer":
        shipping_address=request.form.get('shipping_address')
        shipping_pincode=request.form.get('shipping_pincode')
        shipping_city=request.form.get('shipping_city')
        billing_address=request.form.get('billing_address')
        billing_pincode=request.form.get('billing_pincode')
        billing_city=request.form.get('billing_city')
        email=session['email']#find using this
        cursor.execute("SELECT CustomerId FROM Customer WHERE EmailId LIKE '{}'".format(email))
        Id= cursor.fetchone()[0] #returns a tuple with just  element
        #print(Id)
        query = f"""
            UPDATE Customer
            SET
                ShippingAddress = '{shipping_address}',
                Pincode_Shipping = {shipping_pincode},
                City_Shipping = '{shipping_city}',
                BillingAddress = '{billing_address}',
                Pincode_Billing = {billing_pincode},
                City_Billing = '{billing_city}'
            WHERE CustomerId = {Id};
        """
        cursor.execute(query)
        conn.commit()
        return redirect('/')
    else:
        PaymentInfo=request.form.get('paymentMethod')
        BillingAddress=request.form.get('billingAddress')
        email=session['email']#find using this
        cursor.execute("SELECT SellerId FROM sellerretailer WHERE EmailId LIKE '{}'".format(email))
        Id= cursor.fetchone()[0] #returns a tuple with just  element
        print(Id)
        query = f"""
            UPDATE sellerretailer
            SET
              PaymentInfo='{PaymentInfo}',
              BillingAddress='{BillingAddress}'
            WHERE SellerId = {Id};
        """
        cursor.execute(query)
        conn.commit()
        return redirect('/')

@app.route('/add_product',methods=["POST"])        
def add_product():
    if 'user_id' in session and session['user_type']=='seller':
        title=request.form.get('Title')
        description=request.form.get('description')
        price=request.form.get('price')
        category=request.form.get('category')
        image=request.files.get('image')
        sellerid=session['user_id']
        if image.filename != '':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            #print(filepath)
            filename="../uploads/"+image.filename
            #print(filename)
            
            image.save(filepath)
            #print(filename)
        #print(category)
        cursor.execute("INSERT INTO Product( ProductId,Price,Category,Description,ProductImages,QuantityAvailable,EstimatedDeliveryTime,SellerId,product_name) VALUES (NULL,'{}','{}','{}','{}',NULL,NULL,'{}','{}')".format(price,category,description,filename,sellerid,title))
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
# def products():
#     # Fetch product data from the database
#     cursor.execute("SELECT ProductId, Price, Description, ProductImages, product_name, Category FROM Product")
#     products = cursor.fetchall()

    
    
    
    
#     status = "NO"  # Default status is "NO" if the user is not logged in
#     already_added = {}  # Dictionary to store already added status for each product

#     if 'user_id' in session:
#         status = "YES"
#         CustomerId = session['user_id']

#         for product in products:
#             # Check if the product is already in the user's wishlist
#             cursor.execute("SELECT COUNT(*) FROM wishlist WHERE CustomerID = %s AND ProductId = %s", (CustomerId, product[0]))
#             already_added[product[0]] = cursor.fetchone()[0] > 0

#     return render_template('products.html', products=products, status=status, already_added=already_added,category="All")

def products():
    # Fetch product data from the database
    cursor.execute("SELECT ProductId, Price, Description, ProductImages, product_name, Category FROM Product")
    products = cursor.fetchall()
    if session:
        category=session['category']
    else:
        category="All"    

    
    
    status = "NO"  # Default status is "NO" if the user is not logged in
    already_added = {}  # Dictionary to store already added status for each product

    if 'user_id' in session:
        status = "YES"
        CustomerId = session['user_id']

        for product in products:
            # Check if the product is already in the user's wishlist
            cursor.execute("SELECT COUNT(*) FROM wishlist WHERE CustomerID = %s AND ProductId = %s", (CustomerId, product[0]))
            already_added[product[0]] = cursor.fetchone()[0] > 0

    return render_template('products.html', products=products, status=status, already_added=already_added,category=category)

@app.route('/categories' ,methods=["POST"])
def categories():
    category=request.form.get('category')
    if category:
        session['category']=category    
    print("checkmate")
    return redirect('/products')


@app.route('/add_to_wishlist/<int:ProductId>', methods=['POST'])
def add_to_wishlist(ProductId):
    if not session.get('user_id'):
            return redirect(url_for('login'))
    if session['user_type']=="customer":
        
        CustomerId = session['user_id']
        cursor = conn.cursor()

        # cur = mysql.get_db().cursor()
        cursor.execute("INSERT INTO Wishlist (CustomerId, ProductId) VALUES (%s, %s)", (CustomerId, ProductId))
        # mysql.get_db().commit()
        conn.commit()
        cursor.close()

        return redirect(url_for('products'))
    else:
        session['message']="You need to be a buyer"
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