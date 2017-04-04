import requests
import math
earth_radius = 3960.0  # for miles
import urllib

def get_lat_long(obj):
    addr = obj
    vv = str(addr.get_address())
    encoded_addr = urllib.quote_plus(vv)
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+encoded_addr)
    resp_json_payload = response.json()
    try:
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        long = resp_json_payload['results'][0]['geometry']['location']['lng']
    except:
        lat = ''
        long = ''
    return lat,long
    
def distance(lat1,lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    miles = earth_radius * c
    return miles