from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, 'products.json')

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_products(products):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(products, file, indent=4, ensure_ascii=False)

@app.route('/admin')
def admin_panel():
    products = load_products()
    return render_template('admin.html', products=products)

@app.route('/api/admin/update_quantity', methods=['POST'])
def update_quantity():
    data = request.json
    product_id = int(data['id'])
    new_quantity = int(data['quantity'])

    products = load_products()
    for product in products:
        if product['id'] == product_id:
            product['quantity'] = new_quantity
            break

    save_products(products)
    return jsonify({"status": "success"})

@app.route('/api/admin/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    print(f"[LOG] Удаление товара с ID: {product_id}")
    products = load_products()
    products = [p for p in products if p['id'] != product_id]
    save_products(products)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(port=8080, debug=True)