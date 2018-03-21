from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .models import Station, Request
from json import dumps
from datetime import datetime as dt
from hashlib import sha256
from .utils import get_nearest,get_all_nearest
from random import random

LatLonValidator = lambda x: True if len(x.split(','))==2 and float(x.split(',')[0])\
                            and float(x.split(',')[1]) else False

@csrf_exempt
def StationInsert(request):
    response = {'code':'SOE-404','data':{}}
    if request.method == 'POST':
        StationID = request.POST.get('StationID')
        StationName = request.POST.get('StationName')
        StationArea = request.POST.get('StationArea')
        LatLonTuple = request.POST.get('LatLonTuple')

        try:
            if not LatLonValidator(LatLonTuple):
                response['code'] = 'LATLON-DECODE-ERROR'
                return HttpResponse(dumps(response))
        except:
            response['code'] = 'LATLON-DECODE-ERROR'
            return HttpResponse(dumps(response))

        SPOCUsername = request.POST.get('SPOCUsername')
        SPOCPassword = request.POST.get('SPOCPassword')

        if all([i!=None for i in [StationID, StationName, StationArea,
                                LatLonTuple, SPOCUsername, SPOCPassword]]):
            try:
                Station(
                    StationID=StationID,
                    StationName=StationName,
                    StationArea=StationArea,
                    LatLonTuple=LatLonTuple,
                    SPOCUsername=SPOCUsername,
                    SPOCPassword=sha256(SPOCPassword.encode()).hexdigest()
                ).save()
                response['code'] = 'OK-200'
                return HttpResponse(dumps(response))
            except:
                return HttpResponse(dumps(response))
        else:
            response['code']='NULL-VALUE-500'
            return HttpResponse(dumps(response))
    else:
        response['code'] = '500-METHOD-NOT-ALLOWED'
        return HttpResponse(dumps(response))

@csrf_exempt
def RequestInsert(request):
    response = {'code':'SOE-404','data':{}}
    if request.method=="POST":
        rid = sha256(dt.now().__str__().encode()).hexdigest()
        IncidentType = request.POST.get('IncidentType')
        Image = request.POST.get('Image') or ''
        LatLonTuple = request.POST.get('LatLonTuple')
        DeviceID = request.POST.get('DeviceID')
        try:
            if not LatLonValidator(LatLonTuple):
                response['code'] = 'LATLON-DECODE-ERROR'
                return HttpResponse(dumps(response))
        except:
            response['code'] = 'LATLON-DECODE-ERROR'
            return HttpResponse(dumps(response))
        Details = request.POST.get('Details') or ''

        ll = LatLonTuple.split(',')
        llt = (float(ll[0]),float(ll[1]))
        #print(get_nearest(llt))

        if all([i!=None for i in [rid, IncidentType, LatLonTuple, DeviceID]]):
            try:
                Request(
                    RequestID=rid,
                    IncidentType=IncidentType,
                    Image= Image,
                    LatLonTuple=LatLonTuple,
                    Details=Details,
                    DeviceID = DeviceID
                ).save()
                response['code'] = 'OK-200'
                response['data']['RequestID'] = rid
                return HttpResponse(dumps(response))
            except:
                return HttpResponse(dumps(response))
        else:
            response['code'] = 'NULL-VALUE-500'
            return HttpResponse(dumps(response))
    else:
        response['code'] = '500-METHOD-NOT-ALLOWED'
        return HttpResponse(dumps(response))

@csrf_exempt
def GetRequests(request):
    response = {'code':'SOE-404','data':[]}
    if request.method == "GET":
        DeviceID = request.GET.get('DeviceID')
        if DeviceID is None:
            response['code'] = 'NO_DeviceID'
            return HttpResponse(dumps(response))
        try:
            response['data'] = []
            for i in Request.objects.filter(DeviceID__exact=DeviceID):
                response['data'].append(i.__json__())

            response['code'] = 'OK-200'
            return HttpResponse(dumps(response))
        except:
            return HttpResponse(dumps(response))
    elif request.method == "POST":
        tok = request.POST.get('tok')
        if tok is not None:
            StationID = cache.get(tok)
            # Get the Station object
            StationObj = Station.objects.get(StationID__exact=StationID)
            # Filter out the requests that have been previously accepted by that station

            rList = Request.objects.filter(AcceptedFrom__exact=StationObj)
            data = [i.__json__() for i in rList]
            response['code'] = 'OK-200'
            response['data'] = data
            return HttpResponse(dumps(response))
    else:
        response['code'] = '500-METHOD-NOT-ALLOWED'
        return HttpResponse(dumps(response))

def GetStations(request):
    response = {'code':'SOE-404','data':[]}
    if request.method == "GET":
        LatLonTuple = request.GET.get('Position')
        try:
            if not LatLonValidator(LatLonTuple):
                response['code'] = 'LATLON-DECODE-ERROR'
                return HttpResponse(dumps(response))
        except:
            response['code'] = 'LATLON-DECODE-ERROR'
            return HttpResponse(dumps(response))

        ll = LatLonTuple.split(',')
        llt = (float(ll[0]),float(ll[1]))
        try:
            Stations = get_all_nearest(llt)
            response['code'] = 'OK-200'
            response['data'] = Stations
            return HttpResponse(dumps(response))
        except:
            return HttpResponse(dumps(response))
    else:
        response['code'] = '500-METHOD-NOT-ALLOWED'
        return HttpResponse(dumps(response))

# Apologies for the poor function below
@csrf_exempt
def Login(request):
    if request.method == "POST":
        SPOCUsername = request.POST.get('SPOCUsername')
        SPOCPassword = request.POST.get('SPOCPassword')
        if all([i!=None for i in [SPOCUsername, SPOCPassword]]):
            SPOCPassword = sha256(SPOCPassword.encode()).hexdigest()
            try:
                StationObject = Station.objects.get(SPOCUsername__exact=SPOCUsername,SPOCPassword__exact=SPOCPassword)
                if StationObject:
                # Write logic to generate a random token, save it in redis and return token to user
                # To accept a request Station must send back this token
                # Currently we are using a pickled Dictionary
                    tok = sha256(str(random()).encode()).hexdigest()
                    cache.set(tok,StationObject.StationID)
                    return HttpResponse(tok)
            except Station.DoesNotExist:
                return HttpResponse()
    return HttpResponse()

@csrf_exempt
def Logout(request):
    response = {'code':'SOE-404','data':[]}
    if request.method == "POST":
        token = request.POST.get('tok')
        if token is not None:
            stnID = cache.get(token)
            if  stnID is not None:
                cache.delete(token)
            else:
                response['code'] = '404-NOT-LOGGED-IN'
                return HttpResponse(response)
        return HttpResponse(response)
    return HttpResponse(response)


# From this point on after logging in every request will contain this returned Token
# The Token will fetch the StationID from Redis Cache and return appropriate response.
# If User logs out then Token will be deleted from Redis Cache and No Mapping will be available
# Thus a user that is not logged in can not access any of the APIs
@csrf_exempt
def AcceptRequest(request):
    if request.method == "POST":
        token = request.POST.get('tok')
        RequestID = request.POST.get('rid')
        try:
            # Get the RequestID and Accept Request
            RequestObj = Request.objects.get(RequestID__exact=RequestID)
            RequestObj.isAccepted = True

            StationID = cache.get(token)

            StationObj = Station.objects.get(StationID__exact=StationID)
            RequestObj.AcceptedFrom = StationObj

            RequestObj.save()
            return HttpResponse(dumps({'code':'OK-200','data':{}}))
        except Exception as e:
            print(e)
            return HttpResponse(dumps({'code':'SOE-404','data':{}}))

