from flask import Flask, request, jsonify
import requests
import threading
import time
import logging
from pymongo import MongoClient

logger = logging.getLogger()
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['Kredivo_Dev']

app = Flask(__name__)

def send_confirm(data):
    time.sleep(5)
    print("===== send confirm ====")
    requests.post(
        url='https://api-sandbox-vn.kredivo.com/checkout/update',
        json=data
    )

@app.route('/push_url', methods=['POST'])
def get_user():
    _data = request.get_json()
    print("amount: ", _data['amount'])
    print("discount_amount: ", (_data['discount_amount']))
    print("disbursed_amount: ", _data['disbursed_amount'])
    print('status: ', _data['trx_status'])
    print("order_id: ", _data['order_id'])
    print('time: ', _data['transaction_time'])
    print('message: ', _data['message'])

    print("Signature_Key: ", _data['signature_key'])
    print("Transaction_ID: ", _data['transaction_id'])
    
    x = threading.Thread(target=send_confirm, args=({
        'signature_key': _data.get('signature_key'),
        'transaction_id': _data.get('transaction_id'),
        "status": "settled"
    },))
    x.start()
    db['Kredivo_Dev'].insert_one({
    'amount': float(_data.get('amount')),
    'discount_amount': float(_data.get('discount_amount')),
    'disbursed_amount': float(_data.get('disbursed_amount')),
    'trx_status': _data.get('trx_status'),
    'order_id': _data.get('order_id'),
    'transaction_time': _data.get('transaction_time'),
    'message': _data.get('message'),
    'trans_id': _data.get('transaction_id'),
    'sign_key': _data.get('signature_key'),
    
    })

    return jsonify( {
      "status":"200",
      "message":"OK"
    })

@app.route('/check', methods=['GET'])
def check():
    return jsonify( {
      "status":"OK",
    })

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug = True)