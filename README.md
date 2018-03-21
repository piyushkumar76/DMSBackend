Responses =
{'code':'CODE', 'data':{}}
data can be a dict or a list
data is an empty dict for any POST request

CODE values -

SOE-404 = Some Other Error (Unexpected)
OK-200 = All Clear Success

1. Insert A Station -
  METHOD = POST
  URL = localhost:8000/StationInsert
  Data Parameters =
    (I) StationID
    (I) StationName
    (I) StationArea
    (I) LatLonTuple
    (I) SPOCUsername
    (I) SPOCPassword

    LatLonTuple Format = xx.xxxx,xx.xxxx

    All Data Parameters must be string
    (I) Important Parameter ( i.e. Can't be Null )

2. Insert A Request -
  URL = /RequestInsert
  METHOD = POST
  Data Parameters =
    (I) IncidentType
    (I) LatLonTuple
    (I) DeviceID
    Image
    Details

    LatLonTuple Format = xx.xxxx,xx.xxxx

3. Get Stations -
  URL = localhost:8000/GetStations
  METHOD = GET
  Data Parameters =
    (I) Position ( LatLonTuple )

4. Get Requests -
  URL = localhost:8000/GetRequests
  METHOD = GET
  Data Parameters =
    (I) DeviceID ( Pass Android or iOS Device ID )
