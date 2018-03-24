from requests import get, post
from websocket import WebSocket
from json import loads,dumps
base_url = "localhost"
port = "7890"
def Login():
    data={
    'SPOCUsername':'TEST_USER',
    'SPOCPassword':'TEST_PASS'
    }
    login_url = "http://{}:{}/Login/".format(base_url,port)
    return post(login_url, data=data)

def TESTSocketandRequest(token):
    ws_url = "ws://{}:{}/connectToServer".format(base_url,port)
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
    request_url = "http://{}:{}/RequestInsert/".format(base_url, port)
    data = {
    'IncidentType': 'Fire',
    'LatLonTuple': '28.123123,10.12313',
    'DeviceID': 'lala'
    }
    return post(request_url, data=data)

def Logout(token):
    data ={
        'tok':token
    }
    logout_url = "http://{}:{}/Logout/".format(base_url, port)
    return post(logout_url, data=data)

def TESTAcceptedRequests(tok):
    data = {
    'tok':tok
    }
    url = "http://{}:{}/GetRequests/".format(base_url, port)
    print(post(url, data=data).text)

def TESTAccept(tok, rid):
    data = {
    'tok':tok,
    'rid':rid
    }
    url = "http://{}:{}/AcceptRequest/".format(base_url, port)
    print(post(url, data=data).text)

if __name__ == "__main__":
    print('*Attempting Login*')
    tok = Login().text
    print('*Login Success*')
    print('*Received Token as', tok)
    data = TESTSocketandRequest(tok)
    print('*Got A Notification FOr Request ', data)
    RequestID = data['RequestID']
    print('*Extracting The Request ID and Submit it to acceptance*')
    TESTAccept(tok,RequestID)
    TESTAcceptedRequests(tok)
    print('*Logging Out*')
    Logout(tok)
    print('*Logout Success*')
