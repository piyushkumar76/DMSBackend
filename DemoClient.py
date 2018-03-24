from requests import get, post
from websocket import WebSocket
from json import loads,dumps

def Login():
    data={
    'SPOCUsername':'TEST_USER',
    'SPOCPassword':'TEST_PASS'
    }
    login_url = "http://18.188.41.89:8000/Login/"
    return post(login_url, data=data)

def TESTSocketandRequest(token):
    ws_url = "ws://18.188.41.89:8000/connectToServer"
    ws = WebSocket()
    print('*Connecting Socket*')
    ws.connect(ws_url)
    print('*Sending Login Token To Authenticate Socket Gateway*')
    ws.send(dumps({"tok": token}))
    print('*Socket Connection Status*',ws.recv())
    print('Simulating A Demo Requests')
    TESTRequest()
    print('Request Submitted')
    return loads(ws.recv())

def TESTRequest():
    request_url = "http://localhost:8000/RequestInsert/"
    data = {
    'IncidentType': 'Earthquake',
    'LatLonTuple': '48.123123,10.12313',
    'DeviceID': '13434'
    }
    return post(request_url, data=data)

def Logout(token):
    data ={
        'tok':token
    }
    logout_url = "http://18.188.41.89:8000/Logout/"
    return post(logout_url, data=data)

def TESTAcceptedRequests(tok):
    data = {
    'tok':tok
    }
    url = "http://18.188.41.89:8000/GetRequests/"
    print(post(url, data=data).text)

def TESTAccept(tok, rid):
    data = {
    'tok':tok,
    'rid':rid
    }
    url = "http://18.188.41.89:8000/AcceptRequest/"
    print(post(url, data=data).text)

if __name__ == "__main__":
    TESTRequest()
    # print('*Attempting Login*')
    # tok = Login().text
    # print('*Login Success*')
    # print('*Received Token as', tok)
    # data = TESTSocketandRequest(tok)
    # print('*Got A Notification FOr Request ', data)
    # RequestID = data['RequestID']
    # print('*Extracting The Request ID and Submit it to acceptance*')
    # TESTAccept(tok,RequestID)
    # TESTAcceptedRequests(tok)
    # print('*Logging Out*')
    # Logout(tok)
    # print('*Logout Success*')