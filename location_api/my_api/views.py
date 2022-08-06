# from itertools import combinations_with_replacement
# from msilib.schema import Error
from time import monotonic, time
from django.shortcuts import render, redirect
from my_api.models import Countries, Regions, SubRegions, Continent, RequestsRec, TimeZoneDb
from my_api.serializers import CountrySerializer, RegionSerializer, SubRegionSerializer, ContinentSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone, timedelta
from django.views import View
import pandas as pd
from pathlib import Path

from .login import get_user_profile
import sys
# import datetime
import pytz
import zoneinfo
import json
import requests
import pprint
# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent
def home(request):
    # session = request.GET.get("session_id", None)
    # if session:
    #     user = get_user_profile(session)
    #     if user is None:
    #         return redirect("https://100014.pythonanywhere.com/")
    #     else:
    #         print(user)
    #         response_data = {'error': True, 'status': "not ok","user":user}
    #         return JsonResponse(response_data)
    # else:
    #     return redirect("https://100014.pythonanywhere.com/")
    return render(request, 'api/home.html')
def api(request):
    return render(request, 'api/api.html')
def rec_tz(request):
    wanted_tz = pd.read_csv(BASE_DIR / 'utcDf.csv')
    column_d = ["UTC", "time_zone","country","city"]
    for index, row in wanted_tz.iterrows():
        print(row['UTC'])
        print(row['time_zone'])
        print(row['country'])
        print(row['city'])
        # rec = TimeZoneDb(utc_attained = row['UTC'],timezone_attained= row['time_zone'],
                    # country_attained= row['country'],city_attained= row['city'])
        # rec.save()

        # if index > 10:
        #     break

    response_data = {'error': True, 'status': "not ok"}
    return JsonResponse(response_data)


def get_event_id():
    dd = datetime.now()
    time = dd.strftime("%d:%m:%Y,%H:%M:%S")
    url = "https://100003.pythonanywhere.com/event_creation"
    data = {"platformcode": "FB", "citycode": "101", "daycode": "0",
            "dbcode": "pfm", "ip_address": "192.168.0.41",
            "login_id": "lav", "session_id": "new",
            "processcode": "1", "regional_time": time,
            "dowell_time": time, "location": "22446576",
            "objectcode": "1", "instancecode": "100074", "context": "Access  ",
            "document_id": "3004", "rules": "some rules", "status": "work"
            }


    r = requests.post(url, json=data)
    print("Event Response ")
    print(r.text)
    return r.text
def mongo_create(key_namer, data):
    team_member_id = {"continent":"1075", 'country':"1076","region":"1077","subregion":"1078", "req_resp_messages":"1087"}
    url = "http://100002.pythonanywhere.com/"

    payload = json.dumps({
    "cluster": "nps",
    "database": "dowellnps",
    "collection": key_namer,
    "document": key_namer,
    "team_member_ID": team_member_id[key_namer],
    "function_ID": "ABCDE",
    "command": "insert",
    "field": data,
    "update_field": {
        "order_nos": 21
    },
    "platform": "bangalore"
})
    headers = {
    'Content-Type': 'application/json'
}

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict= json.loads(response.text)
    print(response.text)
    return response_dict

def mongo_update(key_namer, mongo_id,data):
    team_member_id = {"continent":"1075", 'country':"1076","region":"1077","subregion":"1078"}
    url = "http://100002.pythonanywhere.com/"

    payload = json.dumps({
    "cluster": "nps",
    "database": "dowellnps",
    "collection": key_namer,
    "document": key_namer,
    "team_member_ID": team_member_id[key_namer],
    "function_ID": "ABCDE",
    "command": "update",
    "field": {'id':mongo_id},
    "update_field":data,
    "platform": "bangalore"
})
    headers = {
    'Content-Type': 'application/json'
}

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict= json.loads(response.text)
    print(response.text)
    return response_dict


def mongo_read(key_namer, field_val):
    team_member_id = {"continent":"1075", 'country':"1076","region":"1077","subregion":"1078"}
    database = 'dowellnps'
    period='life_time'
    database_details = {
        'database_name': 'mongodb',
        'collection': key_namer,
        'database': database,
        'fields': [field_val]
    }

    url = 'http://100032.pythonanywhere.com/api/targeted_population/'
    # number of variables for sampling rule
    number_of_variables = -1

    """
        period can be 'custom' or 'last_1_day' or 'last_30_days' or 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time'
        if custom is given then need to specify start_point and end_point
        for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average'
        the the value of that selection in 'm_or_A_value'
        error is the error allowed in percentage
    """

    time_input = {
        'column_name': 'Date',
        'split': 'week',
        'period': 'life_time',
        'start_point': '2021/01/08',
        'end_point': '2022/10/25',
    }

    stage_input_list = [
    ]

    # distribution input
    distribution_input={
        'normal': 1,
        'poisson':0,
        'binomial':0,
        'bernoulli':0

    }

    headers = {'content-type': 'application/json'}
    request_data={
        'database_details': database_details,
        'distribution_input': distribution_input,
        'number_of_variable':number_of_variables,
        'stages':stage_input_list,
        'time_input':time_input,
    }
    response = requests.post(url, json=request_data,headers=headers)
    print("type(response.text) in mongo read")
    print(type(response.text))
    print(response.text)

    respons_j = json.loads(response.text)
    print("returinng respons_j['normal']['data'][0]")
    print(respons_j['normal']['data'][0])
    return respons_j['normal']['data'][0]




def eventId_rectifier():
    continents = Continent.objects.all()
    countries = Countries.objects.all()
    regions = Regions.objects.all()
    for country in countries:
        key_namer= 'country'
        mongo_id = country.mongo_id
        data ={
            "eventId":country.event_id
            # "continent":country.name
        }
        print("data to insert")
        print(data)
        print("mongo to insert")
        print(mongo_id)
        re =mongo_update(key_namer, mongo_id,data)
        print("rererererer")
        print(re)
        if re["isSuccess"]:
            print("Continent: "+str(country.name)+" --> insert Id: ")
            # cont = Continent.objects.get(mongo_id=continentsMongoIds[c])
            # cont.event_id = event_id
            # cont.save()
        else:
            print("Continent: "+str(country.name)+" --> error : "+str(re["error"]))
# class CreateLocs
def loc_creator(request):
    # key_namer = "continent"
    # data  = {
    #     # {'isSuccess': True, 'inserted_id': '62bee119cde2907e388cf473'}
    #     # FB1010000000165667662752096307
    #     "continent":"Africa",
    #     "eventId":get_event_id()
    # }
    mongo_id = '62d25e955cc7cec6042b28ab'
    key_namer= 'region'
    data = {
         "continent":"62bebe4cb1989489418cf07b",
         'country':'62d261b95cc7cec6042b2b2d',
         "eventId":get_event_id(),
         'name':'dummy_region_22',
        'lat_lon':'41.294kk° S174.77kk7° E 2222',
        'city_code':'DUR_2',
        'city_area':'02',
         'code':'None',
         'short':'None',
    }
    re = mongo_create(key_namer, data)
    # re = mongo_update(key_namer, mongo_id,data)

    if re["isSuccess"]:
        print("Continent:  --> insert Id: "+str(re["inserted_id"]))
        # print("Continent:  --> insert Id: ")

    else:
        print("Continent:  --> error : "+str(re["error"]))
    return render (request, 'demos/create_locs.html')

class CustomError(Exception):
    pass
class ContinentList(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None, **kwargs):
        status_dict = dict()
        # countries = Countries.objects.all()
        # serializer = CountrySerializer(countries, many=True)
        # status_dict["isSuccess"]=False
        # countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/
        req_dict = {}
        req_dict["request"]="continet-list-request"
        payload = {}
        payload["username"]=kwargs['username']
        payload["sessionId"]=kwargs['sessionId']
        payload["projectCode"]=kwargs['projectCode']
        req_dict["payload"]=str(payload)
        status_dict['req'] = str(req_dict)
##################
        status_dict['url'] = "continents/username/sessionId/projectCode/"
        status_dict['username'] = kwargs['username']
        status_dict['session_id'] = kwargs['sessionId']
        status_dict['project-code'] = kwargs['projectCode']

        try:
            bad_id_list = [1]
            continents = Continent.objects.all().exclude(id__in=bad_id_list)
            serializer = ContinentSerializer(continents, many=True)
            status_dict["isSuccess"]=True
            status_dict["isError"]=False
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_200_OK
            record_re(status_dict)

            return Response(serializer.data)
        except CustomError:
            status_dict["isSuccess"]=False
            status_dict["isError"]=True
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_400_BAD_REQUEST
            record_re(status_dict)

            return Response("Wrong query type '"+kwargs['query_type']+"'", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            status_dict["isSuccess"]=False
            status_dict["isError"]=True
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_400_BAD_REQUEST
            record_re(status_dict)

            return Response("'"+ kwargs['query_value']+"' not in database", status=status.HTTP_400_BAD_REQUEST)

        # return Response(serializer.data)

    def post(self, request, format=None, **kwargs):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryList(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None, **kwargs):
        status_dict = dict()
        # countries = Countries.objects.all()
        # serializer = CountrySerializer(countries, many=True)
        # status_dict["isSuccess"]=False
        # countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/
        req_dict = {}
        req_dict["request"]="country-list-request"
        payload = {}
        payload["username"]=kwargs['username']
        payload["sessionId"]=kwargs['sessionId']
        payload["projectCode"]=kwargs['projectCode']
        req_dict["payload"]=str(payload)
        status_dict['req'] = str(req_dict)
##################
        status_dict['url'] = "countries/username/sessionId/projectCode/"
        status_dict['username'] = kwargs['username']
        status_dict['session_id'] = kwargs['sessionId']
        status_dict['project-code'] = kwargs['projectCode']

        try:
            bad_id_list = [14,8,9,11,13,10,63, 64,16, 15]
            countries = Countries.objects.all().exclude(id__in=bad_id_list)
            serializer = CountrySerializer(countries, many=True)
            status_dict["isSuccess"]=True
            status_dict["isError"]=False
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_200_OK
            record_re(status_dict)

            return Response(serializer.data)
        except CustomError:
            status_dict["isSuccess"]=False
            status_dict["isError"]=True
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_400_BAD_REQUEST
            record_re(status_dict)

            return Response("Wrong query type '"+kwargs['query_type']+"'", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            status_dict["isSuccess"]=False
            status_dict["isError"]=True
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_400_BAD_REQUEST
            record_re(status_dict)

            return Response("'"+ kwargs['query_value']+"' not in database", status=status.HTTP_400_BAD_REQUEST)

        # return Response(serializer.data)

    def post(self, request, format=None, **kwargs):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CountryDetail(APIView):
    """
    Retrieve, update or delete a country instance.
    """
    def get_object(self, kwargs):
        name = False
        code = False
        short_f = False
        # validator_set = {'name','code', 'short'}
        validator_list = ['name','code', 'short']
        # keys_set = set(kwargs.keys())
        print("Kwargs pk")
        print(kwargs)
        if 'name' == kwargs['query_type']:
            name = True
        if 'code'== kwargs['query_type']:
            code = True
        if 'short' == kwargs['query_type']:
            short_f = True
        # valid_set = validator_set.intersection(keys_set)
        # print("keys_set.difference(valid_set)")
        # print(keys_set.difference(valid_set))
        # if len(keys_set.difference(valid_set)) >0:
        if kwargs['query_type'] not in validator_list:
            raise CustomError("Wrong Api Input")

        try:
            if name:
                return Countries.objects.get(name=kwargs['query_value'])
            if code:
                return Countries.objects.get(country_code=kwargs['query_value'])
            if short_f:
                return Countries.objects.get(country_short=kwargs['query_value'])

            # return Countries.objects.get(pk=pk)
        except Countries.DoesNotExist:
            raise Http404("Country Does not exist")

    def get(self, request, format=None,  **kwargs):
        print("Kwargs")
        print(kwargs)
        try:
            country = self.get_object(kwargs)
            serializer = CountrySerializer(country)
            return Response(serializer.data)
        except CustomError:
            return Response("Wrong query type '"+kwargs['query_type']+"'", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("'"+ kwargs['query_value']+"' not in database", status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None, **kwargs):
        country = self.get_object(kwargs)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, **kwargs):
        country = self.get_object(kwargs)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

############################REGION HANDLING################
class RegionList(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        regions = Regions.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegionDetail(APIView):
    """
    Retrieve, update or delete a country instance.
    """
    def get_object(self, kwargs):
        name = False
        code = False
        short_f = False
        pk_f= False
        country = None
        # validator_set = {'name','code', 'short'}
        validator_list = ['name','code', 'short', 'id']
        # keys_set = set(kwargs.keys())
        print("Kwargs pk")
        print(kwargs)
        if 'name' == kwargs['query_type']:
            name = True
        if 'code'== kwargs['query_type']:
            code = True
        if 'short' == kwargs['query_type']:
            short_f = True
        if 'id' == kwargs['query_type']:
            pk_f = True
        # valid_set = validator_set.intersection(keys_set)
        # print("keys_set.difference(valid_set)")
        # print(keys_set.difference(valid_set))
        # if len(keys_set.difference(valid_set)) >0:
        if kwargs['query_type'] not in validator_list:
            raise CustomError("Wrong Api Input")

        try:
            if name:
                country = Countries.objects.get(name=kwargs['query_value'])
            if code:
                country = Countries.objects.get(country_code=kwargs['query_value'])
            if short_f:
                country = Countries.objects.get(country_short=kwargs['query_value'])
            if pk_f:
                return Regions.objects.get(pk=kwargs['query_value'])
                # country = Countries.objects.get(country_short=kwargs['query_value'])
            # return Countries.objects.get(pk=pk)
        except Countries.DoesNotExist:
            raise Http404("Country Does not exist")
        except Countries.MultipleObjectsReturned:
            print("Caught MultipleObjectsReturned")
            if name:
                country = Countries.objects.filter(name=kwargs['query_value'])
            if code:
                country = Countries.objects.filter(country_code=kwargs['query_value'])
            if short_f:
                country = Countries.objects.filter(country_short=kwargs['query_value'])

            return Regions.objects.filter(country__in=country)

            # if pk_f:
                # return Regions.objects.filter(pk=kwargs['query_value'])




        try:
            # country = Countries.objects.get(name=kwargs['pk'])
            return Regions.objects.filter(country=country)


            # return Countries.objects.get(pk=pk)
        except Regions.DoesNotExist:
            raise Http404("Regions for country do not exist")

    def get(self, request, format=None,  **kwargs):
        print("Kwargs")
        print(kwargs)
        status_dict = dict()
        # countries = Countries.objects.all()
        # serializer = CountrySerializer(countries, many=True)

        # status_dict["isSuccess"]=False
        # countries = Countries.objects.all()
        # serializer = CountrySerializer(countries, many=True)

        # status_dict["isSuccess"]=False
        # countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/
        req_dict = {}
        req_dict["request"]="region-list-request"
        payload = {}
        payload["username"]=kwargs['username']
        payload["sessionId"]=kwargs['sessionId']
        payload["projectCode"]=kwargs['projectCode']
        req_dict["payload"]=str(payload)
        status_dict['req'] = str(req_dict)




        # status_dict['username'] = kwargs['username']
        # status_dict['session_id'] = kwargs['sessionId']
        # status_dict['project-code'] = kwargs['projectCode']



        status_dict['url'] = "region/query_type/query_value/username/sessionId/projectCode/"
        status_dict['username'] = kwargs['username']
        status_dict['session_id'] = kwargs['sessionId']
        status_dict['project-code'] = kwargs['projectCode']
        try:
            regions = self.get_object(kwargs)
            serializer = RegionSerializer(regions, many=True)
            status_dict["isSuccess"]=True
            status_dict["isError"]=False
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_200_OK
            record_re(status_dict)
            return Response(serializer.data)
        except CustomError:
            status_dict["isSuccess"]=True
            status_dict["isError"]=False
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_400_BAD_REQUEST
            record_re(status_dict)
            return Response("Wrong query type '"+kwargs['query_type']+"'", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            status_dict["isSuccess"]=True
            status_dict["isError"]=False
            # status_dict["continents"]="Successful"
            status_dict['response'] = status.HTTP_404_NOT_FOUND
            record_re(status_dict)
            return Response("Regions not in database", status=status.HTTP_404_NOT_FOUND)

########################SUBREGION HANDLING###############################################

class SubRegionList(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        countries = Countries.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubRegionDetail(APIView):
    """
    Retrieve, update or delete a country instance.
    """
    def get_object(self, kwargs):
        name = False
        code = False
        short_f = False
        # validator_set = {'name','code', 'short'}
        validator_list = ['name','code', 'short']
        # keys_set = set(kwargs.keys())
        print("Kwargs pk")
        print(kwargs)
        if 'name' == kwargs['query_type']:
            name = True
        if 'code'== kwargs['query_type']:
            code = True
        if 'short' == kwargs['query_type']:
            short_f = True
        # valid_set = validator_set.intersection(keys_set)
        # print("keys_set.difference(valid_set)")
        # print(keys_set.difference(valid_set))
        # if len(keys_set.difference(valid_set)) >0:
        if kwargs['query_type'] not in validator_list:
            raise CustomError("Wrong Api Input")

        try:
            if name:
                return Countries.objects.get(name=kwargs['query_value'])
            if code:
                return Countries.objects.get(country_code=kwargs['query_value'])
            if short_f:
                return Countries.objects.get(country_short=kwargs['query_value'])

            # return Countries.objects.get(pk=pk)
        except Countries.DoesNotExist:
            raise Http404("Country Does not exist")

    def get(self, request, format=None,  **kwargs):
        print("Kwargs")
        print(kwargs)
        try:
            country = self.get_object(kwargs)
            serializer = CountrySerializer(country)
            return Response(serializer.data)
        except CustomError:
            return Response("Wrong query type '"+kwargs['query_type']+"'", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("'"+ kwargs['query_value']+"' not in database", status=status.HTTP_400_BAD_REQUEST)
class TargetFuntion(View):
    database = 'dowellnps'
    period='life_time'
    url = 'http://100032.pythonanywhere.com/api/targeted_population/'
    # number of variables for sampling rule
    number_of_variables = -1

    """
        period can be 'custom' or 'last_1_day' or 'last_30_days' or 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time'
        if custom is given then need to specify start_point and end_point
        for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average'
        the the value of that selection in 'm_or_A_value'
        error is the error allowed in percentage
    """

    time_input = {
        'column_name': 'Date',
        'split': 'week',
        'period': 'life_time',
        'start_point': '2021/01/08',
        'end_point': '2022/10/25',
    }

    stage_input_list = [
    ]

    # distribution input
    distribution_input={
        'normal': 1,
        'poisson':0,
        'binomial':0,
        'bernoulli':0

    }

    headers = {'content-type': 'application/json'}


    def get(self, request, *args, **kwargs):
        checker = {'region': False, 'country': False, 'continent':False}
        database = self.database
        collection = kwargs['collection']
        checker[collection]= True
        fields = [kwargs['fields']]
        mongo_id = kwargs['mongoId']
        name = kwargs['name']
        print("Monogo Id"+str(mongo_id))
        database_details = {
        'database_name': database,
        'collection': collection,
        'database': database,
        'fields': fields
    }
        request_data={
        'database_details': database_details,
        'distribution_input': self.distribution_input,
        'number_of_variable':self.number_of_variables,
        'stages':self.stage_input_list,
        'time_input':self.time_input,
    }
        response = requests.post(self.url, json=request_data,headers=self.headers)
        print("type(response.text)")
        print(type(response.text))
        print(response.text)

        respons_j = json.loads(response.text)
        if mongo_id == "all":
            print("Mongo Id is all")
            if checker["continent"]:
                print("Continent in process")
                for i in respons_j['normal']['data'][0]:
                    i['ID'] = i['_id']
                    i['section'] = collection
                    print(i['ID'])
                    print(i['section'])
                return render(request,'demos/mongo_continents.html',{'records':respons_j['normal']['data'][0], "name":name})
            else:
                response_data = {'error': True, 'status': "not ok"}
                return JsonResponse(response_data)

        else:
            if checker["country"]:
                print("COuntry in process")
                response_list = list()
                for t in respons_j['normal']['data'][0]:
                    temp_dict ={}
                    if 'continent' in t:
                        if t['continent'] == mongo_id:
                            t['ID'] = t['_id']
                            t['section'] = collection
                            response_list.append(t)

                            print(t['ID'])
                            print(t['section'])
                return render(request,'demos/mongo_countries.html',{'records':response_list, 'name':name})


            if checker["region"]:
                print("Region in process")
                response_list2 = list()

                temp_dict ={}
                for v in respons_j['normal']['data'][0]:
                    temp_dict ={}
                    if 'country' in v:
                        if v['country'] == mongo_id:
                            response_list2.append(v)
                            v['ID'] = v['_id']
                            v['section'] = collection
                            print(v['ID'])
                            print(v['section'])
                return render(request,'demos/mongo_regions.html',{'records':response_list2 , 'name':name})
class LocalAccess(View):
    def get(self, request, *args, **kwargs):
        checker = {'region': False, 'country': False, 'continent':False}
        section = kwargs['section']
        # name = kwargs[]
def local_continents(request):
    continents =  Continent.objects.all()
    context = {"records":continents, "name":"All"}
    return render (request, 'demos/local_continents.html',context)
def local_countries(request, pk):
    if pk == 0:
        countries =  Countries.objects.all()
        context = {"records":countries, "name":"All"}
        return render (request, 'demos/local_countries.html',context)
    else :
        try:
            cont =  Continent.objects.get(pk=pk)
            countries =  Countries.objects.filter(continent = cont)
            context = {"records":countries, "name":cont.name}
            return render (request, 'demos/local_countries.html',context)
        except:
            response_data = {'error': True, 'status': "not ok"}
            return JsonResponse(response_data)

def local_regions(request, pk):
    if pk == 0:
        # countries =  Countries.objects.all()
        regions =  Regions.objects.all()
        context = {"records":regions, "name":"All"}
        return render (request, 'demos/local_regions.html',context)
    else :
        try:
            country =  Countries.objects.get(pk=pk)
            regions =  Regions.objects.filter(country = country)
            context = {"records":regions, "name":country.name}
            return render (request, 'demos/local_regions.html',context)
        except:
            response_data = {'error': True, 'status': "not ok"}
            return JsonResponse(response_data)
def date_time_cleaner(to_object, date_t_):
    date_t = str(date_t_)
    if to_object:
        pass
    else:
        print("to_object == False")
        print(date_t[:-6])
        return date_t[:-6]
def date_balancer(db_time):
    print("Passed database time = "+str(db_time))
    #Get current timezone
    utc_dt = datetime.now(timezone.utc) # UTC time
    dt = utc_dt.astimezone() # local time
    print("date_balancer")
    print(dt)
    current_tz = str(dt)[-6:]
    print("current tz = "+current_tz)

    ##Get hrs difference of timezone as dff_hrs and know if plus or minus
    sn = current_tz[0]
    time_hr = current_tz[1:3]
    time_min = current_tz[4:]
    print("current sn = "+sn)
    print("current time_hr = "+time_hr)
    print("current time_min = "+time_min)
    ##Add dff_hrs if plus then minus if minus
    if sn == "+":
        print("time is addition")
        print(int(time_hr))
        print(int(time_min))
        adjusted_date = db_time + timedelta(hours=int(time_hr))
        adjusted_date = adjusted_date + timedelta(minutes=int(time_min))

        # adjusted_date = ts + datetime.timedelta(seconds=1)

    else:
        print("time is subtraction")
        print(int(time_hr))
        print(int(time_min))
        adjusted_date = db_time - timedelta(hours=int(time_hr))
        adjusted_date = adjusted_date - timedelta(minutes=int(time_min))
    print("Adjusted date == "+str(adjusted_date))
    ##COvert to abdijan time
    abdijan_tz = zoneinfo.ZoneInfo('Africa/Abidjan')
    abdinjan_adjusted_time_conv = adjusted_date.astimezone( abdijan_tz)
    print("abdinjan_adjusted_time_conv")
    print(abdinjan_adjusted_time_conv)
    return abdinjan_adjusted_time_conv
def record_re(kwargs):
    print("rerererrererererererererererererererererererererereerererererererererererererererererererereererer")
    print(kwargs)
    print("rerererrererererererererererererererererererererereerererererererererererererererererererereererer")
    abdijan_date = datetime.now(pytz.timezone('Africa/Abidjan'))
    abdijan_time_string = date_time_cleaner(False, str(abdijan_date))
    event_id =  get_event_id()
    payload = {
        "eventId":event_id,
    "request":kwargs['req'],
    "url":kwargs['url'],
    "response":kwargs['response'],
    "username":kwargs['username'],
    "session_id":kwargs['session_id'],
    "isSuccess":kwargs["isSuccess"],
     "isError":kwargs["isError"],
    'project-code': kwargs['project-code'] ,
    "date_time_rec":abdijan_time_string,
    "time_z":'Africa/Abidjan'
        }

    result = mongo_create("req_resp_messages",payload )
    if result["isSuccess"]:
        print("Request:  --> insert Id: "+str(result["inserted_id"]))
        rec = RequestsRec(req=kwargs['req'],url_req=kwargs['url'],response=kwargs['response'],
        username=kwargs['username'],session_id=kwargs['session_id'],date_time_rec=abdijan_time_string,
        mongo_id=result["inserted_id"],event_id=event_id, project_code=kwargs['project-code'],
        is_success=kwargs["isSuccess"],is_error=kwargs["isError"],
        )
        rec.save()
        return True
    else:
        print("Request has an error : "+str(result["error"]))
        return False
    print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")

    # return True
def sync_func(request):
    print("Ebent Id")
    # test_d = {"dhdhdhdhdhd":"dhjsjdgdjsgfjd","uhshsh":"shshshshsh"}
    # print(str(test_d))
    # print(get_event_id())
    us_date = datetime.now(pytz.timezone('US/Pacific'))
    kenya_date = datetime.now(pytz.timezone('Africa/Nairobi'))
    india_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    abdijan_date = datetime.now(pytz.timezone('Africa/Abidjan'))
    conveterd_date =  abdijan_date.astimezone(pytz.timezone('Africa/Cairo'))
    paris_date =  abdijan_date.astimezone(pytz.timezone("Europe/Paris"))
    kenya_time_string = date_time_cleaner(False, str(kenya_date))
    print(type(kenya_date))
    date_time_obj = datetime.strptime(kenya_time_string, '%Y-%m-%d %H:%M:%S.%f')
    print("date_time_obj coming up")
    print(date_time_obj)
    print("us date: "+str(us_date))
    print("kenya date: "+str(kenya_date))

    date_time_cleaner(False, str(us_date))
    paris_tz = zoneinfo.ZoneInfo("Europe/Paris")
    kenya_tz = zoneinfo.ZoneInfo('Africa/Nairobi')
    abdijan_tz = zoneinfo.ZoneInfo('Africa/Abidjan')

    paris_time_conv= date_time_obj.astimezone(paris_tz)
    # random_t = datetime.datetime.strptime(str(kenya_date), '%Y-%m-%d %H:%M:%S.%f')
    print("india date: "+str(india_date))
    print("abdijan date: "+str(abdijan_date))
    print("Converted paris time date: "+str(paris_time_conv))
    print("original paris time :"+str(paris_date))
    url = 'http://100032.pythonanywhere.com/api/targeted_population/'
    # mongo_create(key_namer, data):
    event_id = get_event_id()
    abdijan_time_string = date_time_cleaner(False, str(abdijan_date))
    data = {
        "req":"Insert","url_req":url, "response2":"Looks good2","username":"Programmer",
    "session_id":"292920","date_time_rec":abdijan_time_string, "eventId":event_id, "timeZone":'Africa/Abidjan'
    }
    result = mongo_create("req_resp_messages",data )

    if result["isSuccess"]:
        print("Request:  --> insert Id: "+str(result["inserted_id"]))
        reqrec = RequestsRec(req="Insert",url_req=url, response="Looks good",username="Programmer",
    session_id="292929",date_time_rec=abdijan_time_string,mongo_id=result["inserted_id"],event_id=event_id)
        reqrec.save()
    else:
        print("Request has an error : "+str(result["error"]))
    test_data = RequestsRec.objects.get(mongo_id=result["inserted_id"])
    print("datetime from db before convertion time")
    print(test_data.date_time_rec)
    db_time_obj = datetime.strptime(test_data.date_time_rec[:-7], '%Y-%m-%d %H:%M:%S')
    print("===================================================================================")
    date_balancer(db_time_obj)
    print("===================================================================================")

    print("datetime from db after convertion time")
    print(test_data.date_time_rec)
    print("datetime object after convertion time")
    print(db_time_obj)
    abdinjan_time_conv = date_balancer(db_time_obj)
    print("abdijand time")
    print(abdinjan_time_conv)

    kenyan_time_conv= abdinjan_time_conv.astimezone(kenya_tz)
    print("kenyan time")
    print(kenyan_time_conv)
    print("Database time was "+test_data.date_time_rec[:-7]+" converted time to Kenyan time to: "+str(kenyan_time_conv))






    # print(date_time_obj)




    response_data = {'error': False, 'status': "ok", "abdijan":abdijan_date,
   "data_base_date":test_data.date_time_rec,
   "COnverted Kenyan Date":str(kenyan_time_conv),
     "kenya date":kenya_date,
      "us date":us_date,
     "indian date":india_date}
    return JsonResponse(response_data)
def handle_sync(action):
    ##Continents
    #Local

    local_contis = Continent.objects.all()
    local_contis_list = list()
    for c in local_contis:
        temp_string = c.name+"-"+c.mongo_id
        local_contis_list.append(temp_string)
    local_contis_set = set(local_contis_list)
    #Mongo
    mongo_contis_list = list()
    mongo_contis = mongo_read('continent', 'continent')
    print("mogno contis")
    print(mongo_contis)
    for m in mongo_contis:
        temp_string = m['continent']+"-"+m['_id']
        mongo_contis_list.append(temp_string)
    mongo_contis_set = set(mongo_contis_list)
    ##Difference set
    mongo_contis_difference_set =  mongo_contis_set.difference(local_contis_set)
    local_contis_difference_set =  local_contis_set.difference(mongo_contis_set)
    #Countries
    #Local
    local_countries = Countries.objects.all()
    local_countries_list = list()
    for t in local_countries:
        temp_string = t.name+"-"+t.mongo_id
        local_countries_list.append(temp_string)
    local_countries_set = set(local_countries_list)
    #Mongo
    mongo_countries_list = list()
    mongo_countries = mongo_read('country', 'name')
    print("mongo_countries")
    print(mongo_countries)
    for m in mongo_countries:
        temp_string = m['name']+"-"+m['_id']
        mongo_countries_list.append(temp_string)
    mongo_countries_set = set(mongo_countries_list)
    ##Difference set
    mongo_countries_difference_set =  mongo_countries_set.difference(local_countries_set)
    local_countries_difference_set =  local_countries_set.difference(mongo_countries_set)
        #Regions
    #Local
    local_regions = Regions.objects.all()
    local_regions_list = list()
    for v in local_regions:
        temp_string = v.name+"-"+v.mongo_id
        local_regions_list.append(temp_string)
    local_regions_set = set(local_regions_list)
    #Mongo
    mongo_regions_list = list()
    mongo_regions = mongo_read('region', 'name')
    print("mongo_regions")
    print(mongo_regions)
    regions_black_list= ["62d25e955cc7cec6042b28ab","62d25dce5cc7cec6042b280d"]
    for m in mongo_regions:
        if m['_id'] not in regions_black_list:
            temp_string = m['name']+"-"+m['_id']
            mongo_regions_list.append(temp_string)
    mongo_regions_set = set(mongo_regions_list)
    ##Difference set
    mongo_regions_difference_set =  mongo_regions_set.difference(local_regions_set)
    local_regions_difference_set =  local_regions_set.difference(mongo_regions_set)
    if action =="update":
        #COntinents
        update_conts_ids = list()
        for i in mongo_contis_difference_set:
            print("i")
            print(i)
            p = i.find("-")
            print(p)
            print(i[:p])
            name = i[:p]
            print("------>>>>>>")
            cont_id = i[(p+1):]
            print(i[(p+1):])
            update_conts_ids.append(cont_id)
        print("uopdate_ids")
        print(update_conts_ids)
        for k in mongo_contis:
            status_dict = dict()
            print("k['_id'] "+str(k['_id']))
            if k['_id'] in update_conts_ids:
                print("kkkkk")
                print(k)
                req_dict = {"request":"sync-update", "payload":{"name":k['continent'], "event_id":k['eventId'], "mongo_id": k['_id']},}
                status_dict['req'] = str(req_dict)
                try:
                    cont = Continent(name = k['continent'], event_id=k['eventId'], mongo_id = k['_id'])
                    cont.save()
                    status_dict["isSuccess"]=True
                    status_dict["isError"]=False
                    status_dict["continents"]="Successful"
                    status_dict['response'] = "local continent update successful"

                except:
                    print("Continent not saved ")
                    status_dict["isSuccess"]=False
                    status_dict["isError"]=True
                    status_dict["continents"]="Not Successful"
                    status_dict['response'] = "local continent update NOT successful"


                status_dict['url'] = "local"
                status_dict['username'] = "frontend-programmer"
                status_dict['session_id'] = "devopmentId"
                status_dict['project-code'] = "100074"
                record_re(status_dict)

    #             "req":kwargs['req'],
    # "url":kwargs['url'],
    # "response":kwargs['response'],
    # "username":kwargs['username'],
    # "session_id":kwargs['session_id'],
        #Countries
        update_countries_ids = list()
        for i in mongo_countries_difference_set:
            # print("i")
            # print(i)
            p = i.find("-")
            # print(p)
            # print(i[:p])
            name = i[:p]
            # print("------>>>>>>")
            cont_id = i[(p+1):]
            # print(i[(p+1):])
            update_countries_ids.append(cont_id)
            print("Continent Not found")
        # print("uopdate_ids")
        # print(update_conts_ids)
        for k in mongo_countries:
            status_dict = dict()

            # print("k['_id' countrys] "+str(k['_id']))
            if k['_id'] in update_countries_ids:
                # print("kkkkk countries")
                print(k)
                req_dict = {"request":"sync-update", "payload":{"name":k['name'], "event_id":k['eventId'],
                "mongo_id": k['_id']},
                "country_code":k['country_code'],
                "country_short":k['country_short'],
                "continent":k['continent'],
                }
                status_dict['req'] = str(req_dict)
                try:
                    continent = Continent.objects.get(mongo_id=k['continent'])
                    # print("Continent for countrry above name "+str(continent.name))
                    country = Countries(continent= continent,name=k['name'],country_code=k['country_code'],
                country_short=k['country_short'],mongo_id=k['_id'],event_id=k['eventId'])
                    country.save()
                    status_dict["isSuccess"]=True
                    status_dict["isError"]=False
                    status_dict["regions"]="Successful"
                    status_dict['response'] = "local country update successful"
                except:
                    # print("Continent Not found")
                    # print("Errors gggggg", sys.exc_info())
                    # print(Exception)
                    # print("Errors", sys.exc_info()[0])
                    status_dict["isSuccess"]=False
                    status_dict["isError"]=True
                    status_dict["regions"]="Not Successful"
                    status_dict['response'] = "local country update NOT successful"



                status_dict['url'] = "local"
                status_dict['username'] = "frontend-programmer"
                status_dict['session_id'] = "devopmentId"
                status_dict['project-code'] = "100074"
                record_re(status_dict)
        #Cities
        update_regions_ids = list()
        for i in mongo_regions_difference_set:
            # print("i")
            # print(i)
            p = i.find("-")
            # print(p)
            # print(i[:p])
            name = i[:p]
            # print("------>>>>>>")
            cont_id = i[(p+1):]
            # print(i[(p+1):])
            update_regions_ids.append(cont_id)
        # print("uopdate_ids")
        # print(update_conts_ids)
        for k in mongo_regions:
            status_dict = dict()
            # print("k['_id' regions] "+str(k['_id']))
            if k['_id'] in update_regions_ids:
                # print("kkkkk regions")
                # print(k)
                req_dict = {}
                req_dict["request"]="sync-update"
                payload = {}
                payload["name"]=k['name']
                payload["event_id"]=k['eventId']
                payload["mongo_id"]= k['_id']
                if "country"in k:
                    payload["country"]=k['country']
                else:
                    k['country'] ="Dummy Country"
                    payload["country"]=k['country']

                if "lat_lon"in k:
                    payload["lat_lon"]=k['lat_lon']
                else:
                    k['lat_lon'] ="Lat Long"
                    payload["lat_lon"]=k['lat_lon']
                if "city_code"in k:
                    payload["city_code"]=k['city_code']
                else:
                    k['city_code'] ="City Code"
                    payload["city_code"]=k['city_code']
                if "city_area"in k:
                    payload["city_area"]= k['city_area']
                else:
                    k['city_area'] ="City Area"
                    payload["city_area"]=k['city_area']
                req_dict["payload"]=str(payload)
                # req_dict = {"request":"sync-update", "payload":{"name":k['name'], "event_id":k['eventId'],
                # "mongo_id": k['_id']},
                # "country":k['country'],
                # "lat_lon":k['lat_lon'],
                # "city_code":k['city_code'],
                # "city_area": k['city_area']
                # }
                status_dict['req'] = str(req_dict)
                try:
                    country = Countries.objects.get(mongo_id=k['country'])
                    region = Regions(country= country,name=k['name'],lat_lon=k['lat_lon'],city_code=k['city_code'],
                city_area= k['city_area'],mongo_id=k['_id'],event_id=k['eventId'])
                    region.save()
                    status_dict["isSuccess"]=True
                    status_dict["isError"]=False
                    status_dict["regions"]="Successful"
                    status_dict['response'] = "local country update successful"

                    # print("Country for region above name "+str(continent.name))

                except:
                    print("Continent Not found")
                    print("Errors hhhh", sys.exc_info())
                    print(Exception)
                    print("Errors", sys.exc_info()[0])
                    status_dict["isSuccess"]=False
                    status_dict["isError"]=True
                    status_dict["regions"]="Not Successful"
                    status_dict['response'] = "local country update NOT successful"

                # region = Regions(country= country,name=k['name'],lat_lon=k['lat_lon'],city_code=k['city_code'],
                # city_area= k['city_area'],mongo_id=k['_id'],event_id=k['eventId'])
                # region.save()


                status_dict['url'] = "local"
                status_dict['username'] = "frontend-programmer"
                status_dict['session_id'] = "devopmentId"
                status_dict['project-code'] = "100074"
                record_re(status_dict)

    response_data = {'error': False, 'success':True,'status': "ok", "length_local_contis_set":str(len(local_contis_set)),
        "local_contis_set":str(local_contis_set), "length_mongo_contis_set":str(len(mongo_contis_set)),
        "mongo_contis_set":str(mongo_contis_set),
        "length_mongo_difference_set":str(len(mongo_contis_difference_set)), "mongo_continent_difference_set":list(mongo_contis_difference_set),
        "length_local_difference_set":str(len(local_contis_difference_set)), "local__continent_difference_set":str(local_contis_difference_set),
        "length_mongo_countries_difference_set":str(len(mongo_countries_difference_set)), "mongo_countries_difference_set":list(mongo_countries_difference_set),
        "length_local_countries_difference_set":str(len(local_countries_difference_set)), "local_countries_difference_set":list(local_countries_difference_set),
         "length_mongo_regions_difference_set":str(len(mongo_regions_difference_set)), "mongo_regions_difference_set":list(mongo_regions_difference_set),
         "length_local_regions_difference_set":str(len(local_regions_difference_set)), "local_regions_difference_set":str(local_regions_difference_set),
         }

    return response_data
class SyncFunc(View):
    template_name = 'demos/sync_recs.html'

    def get(self, request, *args, **kwargs):



        response_data = handle_sync("display")

        # return JsonResponse(response_data)
        return render(request, self.template_name,response_data )
    def post(self, request, *args, **kwargs):
        response_data = handle_sync("update")
        pass








        # return render(request, 'demos/log_in_func.html')
def target_func(request):
    # database ='license'
    database = 'dowellnps'
    # collection ='licenses'
    collection='continent'
    # fields = ['function_name']
    fields=['continent']
    # fields={'id':'62bee119cde2907e388cf473'}
    # "field": {'id':mongo_id}
    # period = 'life_time'
    period='life_time'
    url = 'http://100032.pythonanywhere.com/api/targeted_population/'

    database_details = {
        'database_name': database,
        'collection': collection,
        'database': database,
        'fields': fields
    }

    # number of variables for sampling rule
    number_of_variables = -1

    """
        period can be 'custom' or 'last_1_day' or 'last_30_days' or 'last_90_days' or 'last_180_days' or 'last_1_year' or 'life_time'
        if custom is given then need to specify start_point and end_point
        for others datatpe 'm_or_A_selction' can be 'maximum_point' or 'population_average'
        the the value of that selection in 'm_or_A_value'
        error is the error allowed in percentage
    """

    time_input = {
        'column_name': 'Date',
        'split': 'week',
        'period': period,
        'start_point': '2021/01/08',
        'end_point': '2022/10/25',
    }

    stage_input_list = [
    ]

    # distribution input
    distribution_input={
        'normal': 1,
        'poisson':0,
        'binomial':0,
        'bernoulli':0

    }

    request_data={
        'database_details': database_details,
        'distribution_input': distribution_input,
        'number_of_variable':number_of_variables,
        'stages':stage_input_list,
        'time_input':time_input,
    }

    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=request_data,headers=headers)
    print("type(response.text)")
    print(type(response.text))
    print(response.text)

    respons_j = json.loads(response.text)
    # print("respons_j")
    # print(type(respons_j))
    # print("respons_j['normal']")
    # print(type(respons_j['normal']))
    # for i in respons_j['normal']:
    #     print("i: "+str(i))
    #     print("respons_j['normal'][type]")
    #     print(type(respons_j['normal'][i]))
    # for i in respons_j['normal']['data']:
    #     for t in i:
    #         print("t: "+str(t))


    print("Normall data o")
    print(respons_j['normal']['data'][0])
    for i in respons_j['normal']['data'][0]:
        i['ID'] = i['_id']
        print(i['ID'])
    # return response.text
    return render(request,'demos/target_func.html',{'records':respons_j['normal']['data'][0]})
def log_in_func(request):
    return render(request, 'demos/log_in_func.html')
class LoInFunc(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'demos/log_in_func.html')
    def post(self, request, *args, **kwargs):
        loc = request.POST.get("loc", False)
        os = request.POST.get("os", False)
        brow = request.POST.get("brow", False)
        dev = request.POST.get("dev", False)
        time_d = request.POST.get("time", False)
        # drug_category_name = request.POST.get("drug_category_name", False)
        print("loc")
        print(loc)
        print("os")
        print(os)
        print("brow")
        print(brow)
        print("dev")
        print(dev)
        print("time_d")
        print(time_d)
        dd = datetime.now()
        time = dd.strftime("%d:%m:%Y,%H:%M:%S")
        # url = "https://100003.pythonanywhere.com/event_creation"
        username = "dowellFeedback"
        password = "DOWELL@qrcode2022"
        otp="opt"
        ip="192.168.0.41"
        conn="random"
        #  ["otp","loc",dev,"os","brow","time","ip","conn","username","password"]
        url="https://100014.pythonanywhere.com/api/login/"
        userurl="http://100014.pythonanywhere.com/api/user/"
        payload = {"otp": otp, "loc": loc, "dev": dev,
            "os": os, "brow": brow,"time":time,
            "ip": ip, "conn": conn,"username":username,
            "password": password
            }

        r = requests.post(url, json=payload)
        print("=============================Login respomsze======================")
        print(r.text)
        with requests.Session() as s:
            p=s.post(url, data=payload)
            if "Username" in p.text:
                print("p.text")
                print(p.text)
                return p.text
            else:
                user=s.get(userurl)
                print("user.text")
                print(user.text)
                return user.text
        # return r.text
class DisplayReqResp(View):
    def get(self, request, *args, **kwargs):
        # recs = RequestsRec.objects.all()
        time_zones = TimeZoneDb.objects.all()


        return render(request, 'demos/display_req_form_table.html',{"time_zones":time_zones})
    def post(self, request, *args, **kwargs):
        all_ind = request.POST.get("all_ind", False)
        # time_z_selected = request.POST.get("time_z", False)
        time_z_selected_list = request.POST.getlist('time_z')
        time_z_length = len(time_z_selected_list)
        time_z_list = list()
        table_headings = ["username","url","project_code","req","response","session_id","date_time_rec","mongo_id","event_id","is_success","is_error"]

        for i in time_z_selected_list:
            temp_tz=TimeZoneDb.objects.get(id=i)
            country_tz = zoneinfo.ZoneInfo(temp_tz.timezone_attained)
            print("country tz")
            print(country_tz)
            time_z_list.append(temp_tz.timezone_attained)
            table_headings.append(temp_tz.timezone_attained)

        print("all_ind"+str(all_ind))
        print("time_z_selected"+str(time_z_selected_list))
        if all_ind=="all":

            recs = RequestsRec.objects.all()
            recs_list=list()
            for r in recs:
                temp_dict = dict()
                temp_dict["username"] = r.username
                temp_dict["url"] = r.url_req
                temp_dict["project_code"] = r.project_code
                temp_dict["req"] = r.req
                temp_dict["response"] = r.response
                temp_dict["session_id"] = r.session_id
                temp_dict["date_time_rec"] = r.date_time_rec
                temp_dict["mongo_id"] = r.mongo_id
                temp_dict["event_id"] = r.event_id
                temp_dict["is_success"] = r.is_success
                temp_dict["is_error"] = r.is_error
                db_time_obj = datetime.strptime(r.date_time_rec[:-7], '%Y-%m-%d %H:%M:%S')
                abdjian_time = date_balancer(db_time_obj)
                for i in time_z_selected_list:
                    temp_tz=TimeZoneDb.objects.get(id=i)
                    country_tz = zoneinfo.ZoneInfo(temp_tz.timezone_attained)
                    # print("country tz")
                    # print(country_tz)
                    temp_dict[temp_tz.timezone_attained] = abdjian_time.astimezone(country_tz)
                recs_list.append(temp_dict)
                print("time_z_list")
                print(time_z_list)
                    # utc_attained
# country_attained
# city_attained
                    # print()
                # kenyan_time_conv= abdinjan_time_conv.astimezone(kenya_tz
        else:
            pass
        # return render(request, 'demos/display_req_table_ind.html',{"records":recs_list,"time_z_length": str(time_z_length), "time_z_list":time_z_list })
        response_data = {"status":"ok","records":recs_list,"time_z_length": str(time_z_length), "time_z_list":time_z_list, "table_headings":table_headings }
        return JsonResponse(response_data)
class CreateFunc(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'demos/create_locs.html')
    def post(self, request, *args, **kwargs):
        ##Get name of DB
        ##Check if exust in mongo if not then create
        ##Check if exist in local if not create but id exists update mongo_id and event_id

        pass

# Four collections
# COntinent
# Country
# Region
# Town


# "cluster": "Documents",
#  "database": "Documentation",
#  "collection": "TemplateReports",
#  "document": "templatereports",
#  "team_member_ID": "22689044433",
#  "function_ID": "100018",


#  "cluster": "Documents",
#   "database": "Documentation",
#   "collection": "WorkflowReports",
#   "document": "workflowreports",
#   "team_member_ID": "33689044433",
#   "function_ID": "100018",


#   "cluster": "Documents",
#   "database": "Documentation",
#   "collection": "CompanyManagementReports",

#   "document": "companymanagementreports",
#   "team_member_ID": "44689044433",
#   "function_ID": "100018",