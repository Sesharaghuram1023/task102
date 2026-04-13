from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# 🔌 MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sesharaghuramtunuguntla@1023",   # 👉 change this
    database="order_system"
)

cursor = db.cursor()

# 🏠 Home Page (IMPORTANT FIX)
@app.route('/')
def home():
    return render_template('index.html')

# 📦 Place Order
@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json

    name = data['customer_name']
    product = data['product_name']
    quantity = data['quantity']

    sql = "INSERT INTO orders (customer_name, product_name, quantity) VALUES (%s, %s, %s)"
    values = (name, product, quantity)

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Order Placed Successfully"})

# 📋 Get All Orders
@app.route('/orders', methods=['GET'])
def get_orders():
    cursor.execute("SELECT * FROM orders ORDER BY order_id DESC")
    data = cursor.fetchall()
    return jsonify(data)

# 🔄 Update Order Status
@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json

    order_id = data['order_id']
    status = data['status']

    sql = "UPDATE orders SET status=%s WHERE order_id=%s"
    cursor.execute(sql, (status, order_id))
    db.commit()

    return jsonify({"message": "Status Updated"})

# 🚀 Run App
if __name__ == '__main__':
    app.run(debug=True)