from django.shortcuts import render
from my_api.models import Countries, Regions, SubRegions
from my_api.serializers import CountrySerializer, RegionSerializer, SubRegionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class CustomError(Exception):
    pass
class CountryList(APIView):
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
                return Regions.objects.filter(pk=kwargs['query_value'])
                # country = Countries.objects.get(country_short=kwargs['query_value'])
            # return Countries.objects.get(pk=pk)
        except Countries.DoesNotExist:
            raise Http404("Country Does not exist")




        try:         
            # country = Countries.objects.get(name=kwargs['pk'])
            return Regions.objects.filter(country=country)
        

            # return Countries.objects.get(pk=pk)
        except Regions.DoesNotExist:
            raise Http404("Regions for country do not exist")

    def get(self, request, format=None,  **kwargs):
        print("Kwargs")
        print(kwargs)
        try:
            regions = self.get_object(kwargs)
            serializer = RegionSerializer(regions, many=True)
            return Response(serializer.data)
        except CustomError:
            return Response("Wrong query type '"+kwargs['query_type']+"'", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Regions not in database", status=status.HTTP_400_BAD_REQUEST)

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
