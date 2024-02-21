import requests
import http.client
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from decouple import config
nitesh_api_key =  config("NITESH_API_KEY")
class CustomError(Exception):
    pass
def is_string_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
def get_data(data, wanted = "regions", payment=False, offset = 0, limit = 200000000):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    wanted_dets = list()
    data['payment'] = payment

    content_length = len(json.dumps(data))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json", "Content-Length": str(len(data))}
    r=requests.get(url,data=data)
    print("data ------------->",data)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)['data']
        # raw_keys = raw_data.keys()
        # print("raw_data------------->",raw_data)


        wanted_data = list()
        if wanted == "regions":
            count = 0
            counter = 0
            total_entries = len(raw_data)
            wanted_dets.append({"total_number_of_cities":total_entries})
            for i in raw_data:
                if count >= offset and  counter < limit :
                    temp_data = {}
                    temp_data['name']= i['name']
                    temp_data['coordinates']= i['lat_lon']
                    temp_data['lat']= i['lat']
                    temp_data['lon']= i['lon']
                    temp_data['country_code']= i['country_code']
                    temp_data['continent']= i['continent']
                    temp_data['country']= i['country']
                    # temp_data['_id'] = i['_id']
                    wanted_dets.append(temp_data)
                    counter = counter +1
                if  counter >= limit:
                    break
                count = count +1
        else:
            temp_data = {}
            print("raw_data[0]keys", raw_data[0].keys())
            print("raw_data[0]['countries'] type", type(raw_data[0]['countries']))
            print("raw_data[0]['countries']", raw_data[0]['countries'])
            temp_data['countries']= raw_data[0]['countries']
            wanted_dets.append(temp_data)
            # print("iN get data func", {"data": wanted_dets, "success":True})
        return {"data": wanted_dets, "success":True}
        # return Response(serializer.data)
        # print(wanted_data)
    else:
        print(f"Request failed with status code {r.status_code} because {r.text}")
        error_dict = json.loads(r.text)
        return {"success":False, "status_code":{r.status_code}, "message": error_dict['message']}
        # return Response(f"Request failed with status code {r.status_code}", status=status.HTTP_400_BAD_REQUEST)

class GetCoords3(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"status":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            data = request.data
            # api_key = self.request.query_params.get("api_key")
            api_key = nitesh_api_key
            col_name = data['country']
            query = data['query']
            if 'limit' in data and 'offset' in data:
                limit = data['limit']
                offset = data['offset']
                if not is_string_integer(limit):
                    raise CustomError("Use integers only for the limit")
                if not is_string_integer(offset):
                    raise CustomError("Use integers only for the offset")
            if "regionList" in data:
                regions = data['regionList']

            wanted_dets = list()
            if query != "all":
                print("Not All---")
                for i in regions:
                    print("Regions ===> ", i)
#                     payload = {
#     "api_key":"keyu",
#     "operation":"fetch",
#     "db_name":"dowellnps",
#     "coll_name":"italy",
#     "filters":{"name":"Abano Terme"}



# }
                    payload = {
                        "api_key":api_key,
                        "operation":"fetch",
                        "db_name":"dowellnps",
                        "coll_name":col_name,
                        "filters":json.dumps({"name":i})
                        }
                    res = get_data(payload)
                    if res['success']:
                        wanted_dets.extend(res['data'])
                    else:
                        error_message = res['message']
                        raise CustomError(res['message'])
            else:
                print("All---")
                payload = {
                        "api_key":api_key,
                        "operation":"fetch",
                        "db_name":"dowellnps",
                        "coll_name":col_name
                        }
                res = get_data(payload, offset = offset, limit = limit)
                if res['success']:
                    wanted_dets = res['data']
                else:
                    error_message = res['message']
                    raise CustomError(res['message'])
                # wanted_dets = get_data(payload)
                # print("wanted_dets",wanted_dets)
                res = {"data": wanted_dets}
                # print("iN final resp", {"data": wanted_dets})
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the Regions requested. Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)

class GetCoords4(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"status":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            data = request.data
            # api_key = self.request.query_params.get("api_key")
            api_key = nitesh_api_key
            col_name = data['country']
            query = data['query']
            substr = data['subStr']
            # offset = data['offset']
            # if not is_string_integer(limit):
            #     raise CustomError("Use integers only for the limit")
            # if not is_string_integer(offset):
            #     raise CustomError("Use integers only for the offset")
            if "regionList" in data:
                regions = data['regionList']

            wanted_dets = list()
            if query != "all":
                print("Not All---")
                for i in regions:
                    print("Regions ===> ", i)
#                     payload = {
#     "api_key":"keyu",
#     "operation":"fetch",
#     "db_name":"dowellnps",
#     "coll_name":"italy",
#     "filters":{"name":"Abano Terme"}



# }
                    payload = {
                        "api_key":api_key,
                        "operation":"fetch",
                        "db_name":"dowellnps",
                        "coll_name":col_name,
                        "filters":json.dumps({"name":i})
                        # "filters":json.dumps({"name":{"$regex":substr}})
                        }
                    res = get_data(payload)
                    if res['success']:
                        wanted_dets.extend(res['data'])
                    else:
                        error_message = res['message']
                        raise CustomError(res['message'])
            else:
                print("All---")
                payload = {
                        "api_key":api_key,
                        "operation":"fetch",
                        "db_name":"dowellnps",
                        "coll_name":col_name,
                        "filters":json.dumps({"name":{"$regex":substr}})
                        }
                res = get_data(payload)
                if res['success']:
                    wanted_dets = res['data']
                else:
                    error_message = res['message']
                    raise CustomError(res['message'])
                # wanted_dets = get_data(payload)
                # print("wanted_dets",wanted_dets)
                res = {"data": wanted_dets}
                # print("iN final resp", {"data": wanted_dets})
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the Regions requested. Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class GetCountries3(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"status":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            # api_key = self.request.query_params.get("api_key")
            api_key = nitesh_api_key
            wanted_dets = list()
            payload = {
                    "api_key":api_key,
                    "operation":"fetch",
                    "db_name":"dowellnps",
                    "coll_name":"countries_list"
                }
            res = get_data(payload, wanted = "countries")
            if res['success']:
                wanted_dets = res['data']
            else:
                error_message = res['message']
                raise CustomError(res['message'])
            # wanted_dets.extend(get_data(payload))
            res = {"data": wanted_dets}
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the Countries as requested. Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


