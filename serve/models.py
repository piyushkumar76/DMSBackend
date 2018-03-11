from django.db import models
from geopy.distance import distance

class Station(models.Model):
    StationID = models.CharField(max_length=100,primary_key=True)
    StationName = models.CharField(max_length=200)
    StationArea = models.CharField(max_length=200)
    LatLonTuple = models.CharField(max_length=50)
    SPOCUsername = models.CharField(max_length=100)
    SPOCPassword = models.CharField(max_length=100)

    def __str__(self):
        return self.StationID

    def __json__(self):
        ret = {"StationName":self.StationName,"StationArea":self.StationArea,"Location":self.LatLonTuple}
        return ret

    def _get_latlontuple(self):
        parts = self.LatLonTuple.split(',')
        return (float(parts[0]),float(parts[1]))

    def _get_distance(self,LatLonReq):
        return distance(self._get_latlontuple(),LatLonReq).miles

class Request(models.Model):
    RequestID = models.CharField(max_length=100,primary_key=True)
    DeviceID = models.CharField(max_length=100)
    isAccepted = models.BooleanField(default=False)
    IncidentType = models.CharField(max_length=200)
    Image = models.CharField(max_length=100000,null=True)
    LatLonTuple = models.CharField(max_length=50)
    Details = models.CharField(max_length=1000,null=True)
    AcceptedFrom = models.ForeignKey(Station, on_delete = models.CASCADE, null=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.RequestID

    def __json__(self):
        res= {"RequestID":self.RequestID,"IncidentType":self.IncidentType,
                "Details":self.Details, "Image":self.Image, "LatLonTuple":self.LatLonTuple}
        if self.isAccepted:
            res["AcceptedFrom"] = self.AcceptedFrom.StationName
            res['LatLonStation'] = self.AcceptedFrom.LatLonTuple
        return res

    def _get_latlontuple(self):
        parts = self.LatLonTuple.split(',')
        return (float(parts[0]),float(parts[1]))
