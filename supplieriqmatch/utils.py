import requests
import math
earth_radius = 3960.0  # for miles
import urllib
from datetime import datetime

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

def calculate_variable_cost(qty,v_c): 
    variable_cost = 0
    val = v_c.values_list('quantity','cost')
    try:
        cc =filter(lambda x: float(x[0]) <= float(qty),val)
        m = max( [ float(x[0]) for x in cc])
        closest =[b for b in cc if float(b[0]) == m]
        variable_cost = float(closest[0][1]) * float(qty)
    except:
        cc =filter(lambda x: float(x[0]) >= float(qty),val)
        m = min( [ float(x[0]) for x in cc])
        closest =[b for b in cc if float(b[0]) == m]
        variable_cost = float(closest[0][1]) * float(qty)
    
    return variable_cost
    
def calculate_fixed_cost(f_c): 
    fixed_cost = 0
    for x in f_c:
        fixed_cost += float(x.cost)
    return fixed_cost

def calculate_quality(obj):
    try:
        item_reciept_queryset =obj.itemreceipt_set.all()    
        ratings= [x.rating for x in item_reciept_queryset]
        print float(sum(ratings))
        print len(ratings)
        avg_rating = int(sum(ratings)) / len(ratings)
        return avg_rating
    except:
        return "No rating"
    
def calculate_delay_time(item): 
    
    try:
        po_queryset = item.purchaseorder_set.all()
        avg_delay = 0
        for x in po_queryset:
            item_reciept_queryset = x.itemreceipt_set.all()
            avg_delay_for_one_PO = 0
            for y in item_reciept_queryset:
                avg_delay_for_one_PO += (y.date - x.recieve_by_date).days
            avg_delay += int(avg_delay_for_one_PO/item_reciept_queryset.count())
        delay = int(avg_delay/po_queryset.count())
        print delay
         
        if delay > 1:
            return str(delay) + " days"
        elif delay == 0 or delay == 1:
            return str(delay) + " day" 
        else:
            return "No Delay"
#             if abs(delay) > 1:
#                 return str(abs(delay)) + " days before"
#             else:
#                 return str(abs(delay)) + " day before" 
    except:     
        return '0 days'
