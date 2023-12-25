from flask import Flask, render_template, jsonify, request
import qrcode
import os
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class UserOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)


admin = Admin(app, name='Order System', template_mode='bootstrap3')
admin.add_view(ModelView(MenuItem, db.session))

@app.route('/get_menu')
def get_menu():
    menu_items = MenuItem.query.all()
    menu_data = [{'id': item.id, 'name': item.name, 'price': item.price} for item in menu_items]
    return jsonify(menu_data)

@app.route('/')
def index():
    menu = get_menu()
    return render_template('index.html', menu=menu)

@app.route('/order', methods=['POST'])
def order():
    try:
        data = request.get_json()
        selected_items = data.get('selectedItems', [])
        menu_data = get_menu().json
        total_price = sum(item['price'] for item in menu_data if item['id'] in selected_items)

        # 將訂單寫入資料庫
        for item_id in selected_items:
            order = UserOrder(item_id=item_id, quantity=1, total_price=total_price)
            db.session.add(order)
        
        db.session.commit()

        print("Order written to database successfully!")

        return jsonify({"total_price": total_price})
    except Exception as e:
        print(f"Error processing order: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500



@app.route('/qrcode')
def generate_qrcode():
    menu = get_menu()
    url = request.url_root.rstrip('/')  # 取得應用程式的根網址
    img = qrcode.make(url)
    img.save(os.path.join(app.static_folder, 'qrcode.png'))  # 儲存 QR Code 圖片
    return render_template('qrcode.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='192.168.2.24', port=8080)
    app.add_url_rule('/qrcode', 'generate_qrcode', generate_qrcode)
