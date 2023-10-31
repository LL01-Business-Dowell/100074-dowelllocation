import requests
import http.client
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
class CustomError(Exception):
    pass
def get_data(data, wanted = "regions"):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    wanted_dets = list()

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



def data_operation(data):
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    wanted_dets = list()
    content_length = len(json.dumps(data))

    
    headers = {"Content-Type": "application/json", "Content-Length": str(len(data))}
    r=requests.get(url,data=data)
    print("data ------------->",data)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)['data']
        return {"data": raw_data, "success":True}
       
    else:
        print(f"Request failed with status code {r.status_code} because {r.text}")
        error_dict = json.loads(r.text)
        return {"success":False, "status_code":{r.status_code}, "message": error_dict['message']}
        # return Response(f"Request failed with status code {r.status_code}", status=status.HTTP_400_BAD_REQUEST)
 
 
 
def add_collection(formatted_data):
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    r=requests.post(url, formatted_data)
    print("data is here ------------->", formatted_data)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)['data']
        return {"data": raw_data, "success":True}
    
    else:
        print(f"Request failed with status code {r.status_code} because {r.text}")
        error_dict = json.loads(r.text)
        return {"success":False, "status_code":{r.status_code}, "message": error_dict['message']}
        # return Response(f"Request failed with status code {r.status_code}", status=status.HTTP_400_BAD_REQUEST)
 
 
 
 
def deleted_collection(formatted_data):
    print('delete func')
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    r=requests.delete(url, json=formatted_data)
    print("data is here ------------->", formatted_data)
    print("d ------------->", r)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)['data']
        print('This ', raw_data)
        return {"data": raw_data, "success":True}
    
    else:
        print(f"Request failed with status code {r.status_code} because {r.text}")
        error_dict = json.loads(r.text)
        return {"success":False, "status_code":{r.status_code}, "message": error_dict['message']}
        # return Response(f"Request failed with status code {r.status_code}", status=status.HTTP_400_BAD_REQUEST)
 
    
    
 
 
 
 
# def update_collection(formatted_data):
#     print('delete func')
#     url = "https://datacube.uxlivinglab.online/db_api/crud/"
#     r=requests.post(url, data=formatted_data)
#     print("data is here ------------->", formatted_data)
#     print("d ------------->", r)
#     if r.status_code == 201 or r.status_code == 200:
#         raw_data =  json.loads(r.text)['data']
#         print('This ', raw_data)
#         return {"data": raw_data, "success":True}
    
#     else:
#         print(f"Request failed with status code {r.status_code} because {r.text}")
#         error_dict = json.loads(r.text)
#         return {"success":False, "status_code":{r.status_code}, "message": error_dict['message']}
#         # return Response(f"Request failed with status code {r.status_code}", status=status.HTTP_400_BAD_REQUEST)


def update_collection(formatted_data):
    print('update func')
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    
    # The data to be sent should include both query and update_data
    data = {
        "api_key": formatted_data.get("api_key"),
        "db_name": formatted_data.get("db_name"),
        "coll_name": formatted_data.get("coll_name"),
        "operation": formatted_data.get("operation"),
        "query": formatted_data.get("query"),
        "update_data": formatted_data.get("update_data")
    }

    r = requests.post(url, data) 

    print("data is here ------------->", formatted_data)
    print("data is here ------------->", data)
    print("Response ------------->", r)

    if r.status_code == 201 or r.status_code == 200:
        raw_data = json.loads(r.text)['data']
        print('This ', raw_data)
        return {"data": raw_data, "success": True}
    else:
        print(f"Request failed with status code {r.status_code} because {r.text}")
        error_dict = json.loads(r.text)
        return {"success": False, "status_code": r.status_code, "message": error_dict['message']}

# def update_collection(formatted_data):
#     print('update func')
#     url = "https://datacube.uxlivinglab.online/db_api/crud/"
    
#     # The update data should be included in the request body as JSON
#     data = formatted_data  # Just pass the data directly

#     r = requests.post(url, data)  # Use the json parameter to send data as JSON

#     print("data is here ------------->", formatted_data)
#     print("Response ------------->", r)

#     if r.status_code == 201 or r.status_code == 200:
#         raw_data = json.loads(r.text)['data']
#         print('This ', raw_data)
#         return {"data": raw_data, "success": True}
#     else:
#         print(f"Request failed with status code {r.status_code} because {r.text}")
#         error_dict = json.loads(r.text)
#         return {"success": False, "status_code": r.status_code, "message": error_dict['message']}

    
    
    
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
            api_key = self.request.query_params.get("api_key")
            col_name = data['country']
            query = data['query']
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
            api_key = self.request.query_params.get("api_key")
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


   
    



class Collections3(APIView):
    """
    List all countries, or create a new country.
    """
    # def post(self, request, format=None):
    #     return JsonResponse({"status":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            
            
            wanted_dets = list()
            payload = request.data
            print('This is the payload ', payload)
            # {
            #         "api_key":"api_key",
            #         "operation":"fetch",
            #         "db_name":"dowellnps",
            #         "coll_name":"country"
            #     }
            res = data_operation(payload)
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


   

   
    



class AddCollections3(APIView):
    """
    List all countries, or create a new country.
    """
    # def post(self, request, format=None):
    #     return JsonResponse({"status":"Kindly use POST request"})
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            
            
            wanted_dets = list()
            payload = request.data
            print('This is the payload ', payload)
            data_to_insert = payload.get("data")
            formatted_data = {
                "api_key": payload.get("api_key"),  # Replace with your API key
                "db_name": payload.get("db_name"),
                "coll_name": payload.get("coll_name"),
                "operation": payload.get("operation"),
                "data": json.dumps(data_to_insert)
            }
            res = add_collection(formatted_data)
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



    def delete(self, request):
        print('This is the delete function!')
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            
            
            wanted_dets = list()
            payload = request.data
            print('This is the payload ', payload)
            # data_to_insert = payload.get("query")
            query = payload.get("query")
            formatted_data = {
                "api_key": payload.get("api_key"),  # Replace with your API key
                "db_name": payload.get("db_name"),
                "coll_name": payload.get("coll_name"),
                "operation": payload.get("operation"),
                "query": query
            }
            res = deleted_collection(formatted_data)
            if res['success']:
                wanted_dets = res['query']
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


    def put(self, request):
        print('This is the delete function!')
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            
            
            wanted_dets = list()
            payload = request.data
            print('This is the payload ', payload)
            # data_to_insert = payload.get("query")
            query = payload.get("query")
            formatted_data = {
                "api_key": payload.get("api_key"),  # Replace with your API key
                "db_name": payload.get("db_name"),
                "coll_name": payload.get("coll_name"),
                "operation": payload.get("operation"),
                "query": query
            }
            res = update_collection(formatted_data)
            if res['success']:
                wanted_dets = res['query']
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



   
 