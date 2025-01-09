import logging
import os
from flask import Flask, render_template, request

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product-list')
def product():
    return render_template('product-list.html')

@app.route('/product-detail')
def product_detail():
    return render_template('product-detail.html')
    

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)