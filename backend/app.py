from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, 'products.json')

def load_products():
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.route('/')
def index():
    products = load_products()
    return render_template('index.html', products=products)

@app.route('/api/products')
def get_products():
    products = load_products()
    return jsonify(products)

if __name__ == '__main__':
    app.run(port=3000, debug=True)