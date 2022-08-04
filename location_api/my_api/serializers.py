from .models import *
from rest_framework import serializers
class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ['id','name','mongo_id', 'event_id']
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ['id','name', 'country_code','country_short']
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id','name', 'country']
class SubRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRegions
        fields = ['id','name', 'regions']
