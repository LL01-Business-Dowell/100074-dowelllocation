import requests
import http.client
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
class CustomError(Exception):
    pass
def get_data(data):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    wanted_dets = list()
    data = {
    "api_key":"783ae055-6844-4a73-8be7-20b6a157ab9c",
    "operation":"fetch",
    "db_name":"dowellnps",
    "coll_name":"italy",
    "filters":{"name":"Abano Terme"}



}
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
        print("raw_data------------->",raw_data)

        wanted_data = list()
        for i in raw_data:
            temp_data = {}
            temp_data['name']= i['name']
            temp_data['coordinates']= i['lat_lon']
            temp_data['lat']= i['lat']
            temp_data['lon']= i['lon']
            temp_data['country_code']= i['country_code']
            temp_data['continent']= i['continent']
            temp_data['country']= i['country']
            wanted_dets.append(temp_data)
        return wanted_dets
        # print(wanted_data)
    else:
        print(f"Request failed with status code {r.status_code}")
        return wanted_dets

class GetCoords3(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"status":"Kindly use POST request"})
    def post(self, request):
        try:
            data = request.data
            api_key = self.request.query_params.get("api_key")
            col_name = data['country']
            query = data['query']
            if "regionList" in data:
                regions = data['regionList']
            wanted_dets = list()
            if query != "all":
                print("Not All---")
                for i in regions:
                    payload = {
                        "api_key":api_key,
                        "operation":"fetch",
                        "db_name":"dowellnps",
                        "coll_name":col_name,
                        "filters":{"name":i}
                        }
                    wanted_dets.extend(get_data(payload))
            else:
                print("All---")
                payload = {
                        "api_key":api_key,
                        "operation":"fetch",
                        "db_name":"dowellnps",
                        "coll_name":col_name
                        }
                wanted_dets = get_data(payload)
                print("wanted_dets",wanted_dets)
            res = {"data": wanted_dets}
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response("No results for the Regions rquested.", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the Regions rquested.", status=status.HTTP_400_BAD_REQUEST)


