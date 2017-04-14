from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status, viewsets,generics
from rest_framework.response import Response
from supplieriq.serializers import SignInSerializer,VendorSerializer,ItemSerializer,ItemVendorSerializer,CostSerializer,FixedCostSerializer,VariableCostSerializer
from django.contrib.auth.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from supplieriq.models import CompanyVendor,Company, CompanyItem, VendorAddress,Price,FixedCost,VariableCost,ItemVendor,Location,UserCompanyModel,PurchaseOrder,ItemReceipt
from django.shortcuts import render_to_response
import json
from supplieriqmatch.utils import get_lat_long,distance,calculate_quality,\
    calculate_fixed_cost,calculate_variable_cost,calculate_delay_time


# Create your views here.
class MatchAPI(APIView):
    
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def get(self, request,*args, **kwargs):   
        try:     
            cost = {}
            item_id = request.query_params['item']            
            qty = request.query_params['quantity']      
            loc_id = request.query_params['company_address']      
            loc = Location.objects.get(id = loc_id)  
            lat1,long1 = get_lat_long(loc)    
            obj = ItemVendor.objects.filter(companyitem_id = item_id)
            qq = []
            for item in obj:                
                f_c = item.fixedcost_set.all()
                v_c = item.variablecost_set.all()
                fixed_cost = 0
                variable_cost = 0
                if f_c:
                    fixed_cost = calculate_fixed_cost(f_c)
                if v_c:
                    variable_cost = calculate_variable_cost(qty,v_c)

                if variable_cost != 0 and fixed_cost != 0:
                    zzzz=request.user.usercompanymodel_set.all()
                    qqq =zzzz[0]
                    if qqq.company == item.companyvendor.company:
                        total= round(fixed_cost,2) + round(variable_cost,2)                
                        serializer = VendorSerializer(item.companyvendor)
                        
                        # find distance
                        v_addr = item.companyvendor.vendoraddress_set.first()
                        lat2,long2 = get_lat_long(v_addr)                        
                        if lat1 and long1 and lat2 and long2:
                            dist = distance(lat1,long1, lat2, long2)
                        else:
                            if lat1=='' or long1=='':
                                dist = 'Incorrect Company Address..!!'
                            else:
                                dist = 'Incorrect Vendor Address..!!'
                        
                        zz = serializer.data                    
                        zz.update({"total price":float(total)})
                        zz.update({"distance":dist})
                        
                        # find quality
                        quality = calculate_quality(item)

                        #find delay
                        delay = calculate_delay_time(item)
                        
                        zz.update({"quality":quality})
                        zz.update({"delivery delay":delay})
                        zz.update({"itemvendor":item.id})
                    
                        qq.append(zz)
            return Response({'serializer':qq,'item_id':item_id,'quantity':qty},template_name="match_results.html")
        except:
            queryset = CompanyItem.objects.all()
#             serializer = ItemVendorSerializer(queryset, many=True)    
                     
            return Response({'serializer':queryset},template_name="match_results.html")

