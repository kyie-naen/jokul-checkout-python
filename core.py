import hashlib
import hmac
import base64
import requests
import json

# Help for generate signature Request payment
#  @param json body
#  @param string clientId
#  @param string secretKey
#  @return string HMACSHA256
def signatureReq(body, client, clientSecret, server, timeStamp, reqId, pathReq):
    y = json.dumps(body)
    digest = base64.b64encode(hashlib.sha256(y.encode('utf-8')).digest()).decode("utf-8")

    componentSignature = "Client-Id:" + client
    componentSignature += "\n"
    componentSignature += "Request-Id:" + reqId
    componentSignature += "\n"
    componentSignature += "Request-Timestamp:" + timeStamp
    componentSignature += "\n"
    componentSignature += "Request-Target:" + pathReq
    componentSignature += "\n"
    componentSignature += "Digest:" + digest

    message = bytes(componentSignature, 'utf-8')
    secret = bytes(clientSecret, 'utf-8')

    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
    # print(signature)
    return "HMACSHA256="+signature

# Help for Hit jokul API
#  @param json body
#  @param string clientId
#  @param string secretKey
#  @return string HMACSHA256
def hitApi(body, client, clientSecret, server, timeStamp, reqId, signature):
    if server == 'Sandbox':
        url = 'https://api-sandbox.doku.com/checkout/v1/payment'
    else:
        url = 'https://api.doku.com/checkout/v1/payment'

    headers = { "Content-Type": "application/json", "Client-Id": client, "Request-Id": reqId, "Request-Timestamp": timeStamp, "Signature": signature}

    try:
        result = requests.post(url, headers=headers, data=json.dumps(body))
        return result.text
    except requests.exceptions.RequestException as e:
        return "Failed!"
