from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status, viewsets,generics
from rest_framework.response import Response
from supplieriq.serializers import SignInSerializer,VendorSerializer,ItemSerializer,ItemVendorSerializer,CostSerializer,FixedCostSerializer,VariableCostSerializer
from django.contrib.auth.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from supplieriq.models import CompanyVendor,Company, CompanyItem, Address,Price,FixedCost,VariableCost,ItemVendor,UserCompanyModel
from django.shortcuts import render_to_response
import json


# Create your views here.
class MatchAPI(APIView):
    
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def get(self, request,*args, **kwargs):   
        try:     
            cost = {}
            item_id = request.query_params['item']            
            qty = request.query_params['quantity']            
            obj = ItemVendor.objects.filter(companyitem_id = item_id)
            qq = []
            for item in obj:                
                f_c = item.fixedcost_set.all()
                v_c = item.variablecost_set.all()
                fixed_cost = 0
                variable_cost = 0
                if f_c:
                    for x in f_c:
                        fixed_cost += int(x.cost)
                if v_c:
                    val = v_c.values_list('quantity','cost')
                    try:
                        cc =filter(lambda x: int(x[0]) <= int(qty),val)
                        m = max( [ int(x[0]) for x in cc])
                        closest =[b for b in cc if int(b[0]) == m]
                        variable_cost = int(closest[0][1]) * int(qty)
                    except:
                        cc =filter(lambda x: int(x[0]) >= int(qty),val)
                        m = min( [ int(x[0]) for x in cc])
                        closest =[b for b in cc if int(b[0]) == m]
                        variable_cost = int(closest[0][1]) * int(qty)
                if variable_cost != 0 and fixed_cost != 0:
                    zzzz=request.user.usercompanymodel_set.all()
                    qqq =zzzz[0]
                    if qqq.company == item.companyvendor.company:
                        total= fixed_cost + variable_cost                
                        serializer = VendorSerializer(item.companyvendor)
                        zz = serializer.data                    
                        zz.update({"total price":total})
                        zz.update({"itemvendor":item.id})
                        qq.append(zz)
            return Response({'serializer':qq,'item_id':item_id,'quantity':qty},template_name="match_results.html")
        except:
            queryset = CompanyItem.objects.all()
#             serializer = ItemVendorSerializer(queryset, many=True)    
                     
            return Response({'serializer':queryset},template_name="match_results.html")
