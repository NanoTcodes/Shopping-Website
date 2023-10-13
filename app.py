from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

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
    return render_template('sell.html')

@app.route('/login')
def login():
    return render_template('loginpage.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)

