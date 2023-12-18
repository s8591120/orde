from flask import Flask, render_template, jsonify, request
import qrcode
import os

app = Flask(__name__)

menu = [
    {"id": 1, "name": "Item 1", "price": 10.0},
    {"id": 2, "name": "Item 2", "price": 15.0},
    {"id": 3, "name": "Item 3", "price": 20.0},
]

@app.route('/')
def index():
    return render_template('index.html', menu=menu)

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    selected_items = data.get('selectedItems', [])
    total_price = sum(item['price'] for item in menu if item['id'] in selected_items)
    return jsonify({"total_price": total_price})

@app.route('/qrcode')
def generate_qrcode():
    url = request.url_root.rstrip('/')  # 取得應用程式的根網址
    img = qrcode.make(url)
    img.save(os.path.join(app.static_folder, 'qrcode.png'))  # 儲存 QR Code 圖片
    return render_template('qrcode.html')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.2.24', port=8080)
    app.add_url_rule('/qrcode', 'generate_qrcode', generate_qrcode)
