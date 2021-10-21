from flask import Flask, request
from flask_cors import CORS
import datetime

from core import signatureReq, hitApi

app = Flask(__name__)
CORS(app)

@app.route('/request', methods=['POST'])
def requestPayment():
    time = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    invoice = 'INV_d'
    timeStamp = time+'Z'
    reqId = 'req'+time
    pathReq = '/checkout/v1/payment'

    params = request.get_json()
    body = {
        "order" : {
            "amount": params['amount'],
            "invoice_number": invoice,
            "currency": "IDR",
            "callback_url": 'https://doku.com/'
        },
        "payment": {
            "payment_due_date" : 60
        },
        "customer": {
            "id" : "123123123",
            "name" : "Rizky",
            "email" : "rizky.zulkarnaen@doku.com",
            "phone" : "6287805586273",
            "address" : "Jakarta",
            "country" : "ID"
        }
    }
    signature = signatureReq(body, params['client'], params['clientSecret'], params['server'], timeStamp, reqId, pathReq)
    resultPayment = hitApi(body, params['client'], params['clientSecret'], params['server'], timeStamp, reqId, signature)
    return resultPayment
    # return data;

if __name__ == '__main__':
    app.run(debug=True )
