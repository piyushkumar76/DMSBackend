from .models import Station

def get_nearest(latLonReq):
    Nearest = {'stnObject':None, 'distance':999999}
    allStations = Station.objects.all()
    for i in allStations:
        temp_distance = i._get_distance(latLonReq)
        if  temp_distance < Nearest['distance']:
            Nearest['stnObject'] = i
            Nearest['distance'] = temp_distance
    return Nearest

def get_all_nearest(latLonReq):
    StationList = []
    allStations = Station.objects.all()
    for i in allStations:
        StationList.append({"stnObject":i.__json__(),"distance":i._get_distance(latLonReq)})
    StationList.sort(key=lambda i:i["distance"])
    return StationList
