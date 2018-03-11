from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Station, Request
from json import dumps
from datetime import datetime as dt
from hashlib import sha256
from .utils import get_nearest,get_all_nearest

LatLonValidator = lambda x: True if len(x.split(','))==2 and float(x.split(',')[0])\
                            and float(x.split(',')[1]) else False

@csrf_exempt
def StationInsert(request):
    if request.method == 'POST':
        response = {'code':'SOE-404','data':{}}
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
                    SPOCPassword=SPOCPassword
                ).save()
                response['code'] = 'OK-200'
                return HttpResponse(dumps(response))
            except:
                return HttpResponse(dumps(response))
        else:
            response['code']='NULL-VALUE-500'
            return HttpResponse(dumps(response))

@csrf_exempt
def RequestInsert(request):
    if request.method=="POST":
        response = {'code':'SOE-404','data':{}}

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

def GetRequests(request):
    if request.method == "GET":
        DeviceID = request.GET.get('DeviceID')
        response = {'code':'SOE-404','data':{}}
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

def GetStations(request):
    if request.method == "GET":
        response = {'code':'SOE-404','data':{}}
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
