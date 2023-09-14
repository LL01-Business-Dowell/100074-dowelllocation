from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContinentForm ,CountriesForm, RegionsForm, SubRegionsForm
from django.http import Http404, JsonResponse
from my_api.models import Countries, Regions, SubRegions, Continent, RequestsRec, Countries2, Regions2
from .foreign_data import country_mapper, continent_mapper, write_locs, read_locs, del_locs, mongo_create, continent_name_mapper, get_event_id
from .f2 import country_data, cont_id_dict, region_data
from datetime import datetime, timezone, timedelta
import requests
def create_continent(request):
    if request.method == 'POST':
        form = ContinentForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the data to the database
            resp = {"Succesfull":True}
            form = ContinentForm()
            return render(request, 'demos/form_template.html', {'form': form, "success":True, "continentForm":True})
    else:
        form = ContinentForm()

    return render(request, 'demos/form_template.html', {'form': form, "continentForm":True})

def create_country(request):
    if request.method == 'POST':
        data = request.POST
        # form = CountriesForm(data)
        name = data.get('name')
        country_code=data.get('country_code')
        country_short =data.get('country_short')
        cnt_id = data.get("continent")
        continent = Continent.objects.get(pk = cnt_id)
        cont = continent_name_mapper[continent.name]

        print("name ====>>>>", name)
        if not Countries.objects.filter(name=name).exists():
            # if form.is_valid():
            event_id = get_event_id()
            mongo_payload =     {
         "continent": cont,
         "eventId": event_id,
         "name": name,
        "country_code": str(country_code),
        "country_short":str(country_short)
        # 'isSuccess': True, 'inserted_id': '64eae745e67825e7c0bb3e29'}
    }
            response = mongo_create("country", mongo_payload)
            mongo_id = response['inserted_id']
            print("mongo_payload country ===>>>>", mongo_payload)
            cntry = Countries(
                continent = continent,
                name=name,
                country_code =country_code,
                country_short = country_short,
                event_id = event_id,
                mongo_id =mongo_id )
            cntry.save()

            # form.save()  # Saves the data to the database
            resp = {"success":True, "error":False}
            form = CountriesForm()
            return render(request, 'demos/form_template.html', {'form': form, "success":True, "countryForm":True})
            # else:
                # return render(request, 'demos/form_template.html', {'form': form, "error":True, "message":"Error occured during entry of country","countryForm":True})
        else:
            form = CountriesForm()
            return render(request, 'demos/form_template.html', {'form': form, "error":True, "message":"Country exists already","countryForm":True})
    else:
        form = CountriesForm()

    return render(request, 'demos/form_template.html', {'form': form, "countryForm":True})


def create_region(request):
    if request.method == 'POST':
        data = request.POST
        print("type pf data ===>>>>", type(data))
        print("data ===>>>>", data)
        name = data.get('name')
        cnt_id = data.get("country")
        city_code =  data.get("city_code")
        city_area = data.get("city_area")
        #Extras
        lat_value =  data.get("lat_value")
        lat_direction =  data.get("lat_direction")
        lon_value =  data.get("lon_value")
        lon_direction = data.get("lon_direction")
        country = Countries.objects.get(pk = cnt_id)
        print("country ===>>>>", country.name)
        print("country.mongo_id ===>>>>", country.mongo_id)
        print("continent ===>>>>", country.continent)

        lat_lon = f"{lat_value} {lat_direction} {lon_value} {lon_direction}"
        lat_lon_2 = f"{lat_value.strip()[: -1]}  {lon_value.strip()[: -1]}"
        print("lat_lon_2===>>>>", lat_lon_2)
        continent = str( country.continent)

        # form = RegionsForm(request.POST)
        # form = True
        payload = {
            name.lower(): [lat_lon,country.name , continent]
            }

        print("Payload ===>>>>", payload)
        # continent = Countries.objects.get(name = country)
        if not Regions.objects.filter(name=name).exists():
            print("region not presersnt===")
            # if form:
            event_id = get_event_id()
            write_locs(payload)
            cont = continent_name_mapper[continent]
            mongo_payload = {
                'eventId': event_id,

                 'continent': cont,
                   'country': str(country.mongo_id),
                 'name': str(country.name),
                   'lat_lon': lat_lon_2,
                     'city_code': city_code,
                       'city_area':city_area
                      }
            print("mongo_payload region===>>>>", mongo_payload)
            response =  mongo_create("region", mongo_payload)
            mongo_id = response['inserted_id']
            print("mongo_id region===>>>>", mongo_id)
            reg = Regions(
                country=country,
                name=name,
                lat_lon=lat_lon_2,
                city_code= city_code,
                city_area=city_area,
                mongo_id= mongo_id,
                event_id=event_id
                )
            reg.save()
            # form.save()  # Saves the data to the database
            resp = {"Succesfull":True}
            form = RegionsForm()
            return render(request, 'demos/test_form_2.html', {'form': form, "success":True, "regionForm":True})
            # else:
                # return render(request, 'demos/form_template.html', {'form': form, "error":True, "message":"Error occured during entry of city","regionForm":True})

        else:
            form = RegionsForm()
            return render(request, 'demos/test_form_2.html', {'form': form, "error":True, "message":"City exists already","regionForm":True})
    else:
        form = RegionsForm()

    return render(request, 'demos/test_form_2.html', {'form': form, "regionForm":True})
def get_loc_(lat_lon):
    culprit = lat_lon.strip()
    offset = culprit.find("N")
    if offset != -1:
        lat_val = culprit[:offset].strip()
        lat_dir = "N"
    else:
        offset = culprit.find("S")
        if offset != -1:
            lat_val = culprit[:offset].strip()
            lat_dir = "S"
        else:
            offset = culprit.find(" ")
            lat_val = culprit[:offset].strip()
            if lat_val[0] == "-":
                lat_dir = "S"
            else:
                lat_dir = "N"

    culprit = culprit[offset+1:]
    culprit = culprit.strip()
    offset = culprit.find("E")
    if offset != -1:
        lon_val = culprit[:offset].strip()
        lon_dir = "E"
    else:
        offset = culprit.find("W")
        if offset != -1:
            lon_val = culprit[:offset].strip()
            lon_dir = "W"
        else:
            # offset = culprit.find(" ")
            lon_val = culprit
            if lon_val[0] == "-":
                lon_dir = "W"
            else:
                lon_dir = "E"

    return lat_val, lat_dir, lon_val, lon_dir


def update_region(request , pk):
    instance = get_object_or_404(Regions, pk=pk)
    form = RegionsForm( instance=instance)
    if request.method == 'GET':
        lat_lon =  instance.lat_lon
        print("lat_lon --> ", lat_lon)
        print("results ====>>>>", get_loc_(lat_lon))
        lat_value,lat_direction,lon_value,lon_direction,=get_loc_(lat_lon)
        context =     {
        "pk" :  instance.pk,
        "name" :  instance.name,
        "city_code" :  instance.city_code,
        "city_area" :  instance.city_area,
        "lat_value" :  lat_value,
        "lat_direction" :  lat_direction,
        "lon_value" :  lon_value,
        "lon_direction" :  lon_direction,
        "country" :  instance.country,
        }
        return render(request, 'demos/update_region.html', {'form': form, "context":context, "regionForm":True})


    if request.method == 'POST':
        data = request.POST
        print("type pf data ===>>>>", type(data))
        print("data ===>>>>", data)
        # pk =  data.get("id")
        name = data.get('name')
        cnt_id = data.get("country")
        city_code =  data.get("city_code")
        city_area = data.get("city_area")
        #Extras
        lat_value =  data.get("lat_value")
        lat_direction =  data.get("lat_direction")
        lon_value =  data.get("lon_value")
        lon_direction = data.get("lon_direction")
        country = Countries.objects.get(pk = cnt_id)
        print("country ===>>>>", country.name)
        print("country.mongo_id ===>>>>", country.mongo_id)
        print("continent ===>>>>", country.continent)

        lat_lon = f"{lat_value} {lat_direction} {lon_value} {lon_direction}"
        lat_lon_2 = f"{lat_value.strip()[: -1]}  {lon_value.strip()[: -1]}"
        print("lat_lon_2===>>>>", lat_lon_2)
        continent = str( country.continent)

        # form = RegionsForm(request.POST)
        # form = True
        payload = {
            name.lower(): [lat_lon,country.name , continent]
            }

        print("Payload ===>>>>", payload)
        instance.name =name
        instance.cnt_id =cnt_id
        instance.city_code =city_code
        instance.city_area =city_area
        instance.country =country
        instance.lat_lon = lat_lon
        instance.save()
        # continent = Countries.objects.get(name = country)
        # if not Regions.objects.filter(name=name).exists():
        #     print("region not presersnt===")
        #     # if form:
        #     event_id = get_event_id()
        #     write_locs(payload)
        #     cont = continent_name_mapper[continent]
        #     mongo_payload = {
        #         'eventId': event_id,

        #          'continent': cont,
        #           'country': str(country.mongo_id),
        #          'name': str(country.name),
        #           'lat_lon': lat_lon_2,
        #              'city_code': city_code,
        #               'city_area':city_area
        #               }
        #     print("mongo_payload region===>>>>", mongo_payload)
        #     response =  mongo_create("region", mongo_payload)
        #     mongo_id = response['inserted_id']
        #     print("mongo_id region===>>>>", mongo_id)
        #     reg = Regions(
        #         country=country,
        #         name=name,
        #         lat_lon=lat_lon_2,
        #         city_code= city_code,
        #         city_area=city_area,
        #         mongo_id= mongo_id,
        #         event_id=event_id
        #         )
        #     reg.save()
        #     # form.save()  # Saves the data to the database
        #     resp = {"Succesfull":True}
        form = RegionsForm()
        return render(request, 'demos/update_region.html', {'form': form, "success":True, "regionForm":True})
            # else:
                # return render(request, 'demos/form_template.html', {'form': form, "error":True, "message":"Error occured during entry of city","regionForm":True})

        # else:
        #     form = RegionsForm()
        #     return render(request, 'demos/form_template.html.html', {'form': form, "error":True, "message":"City exists already","regionForm":True})
    else:
        form = RegionsForm()

    return render(request, 'demos/update_region.html', {'form': form, "regionForm":True})
def create_sub_region(request):
    if request.method == 'POST':
        data = request.POST
        form = SubRegionsForm(data)
        if form.is_valid():
            form.save()  # Saves the data to the database
            resp = {"Succesfull":True}
            form = SubRegionsForm()
            return render(request, 'demos/form_template.html', {'form': form, "success":True, "subRegionForm":True})
    else:
        form = SubRegionsForm()

    return render(request, 'demos/form_template.html', {'form': form, "subRegionForm":True})

def my_form_test(request):
    # temp_id = cont_id_dict[country_data[15]["continent"]][1]
    # cont = Continent.objects.get(pk=temp_id)
    alread_stored = dict()
    # for country in country_data:
    #     temp_id = cont_id_dict[country["continent"]][1]
    #     temp_continent=Continent.objects.get(pk=temp_id)
    #     temp_name = country["name"]
    #     temp_country_code = country["country_code"]
    #     temp_country_short = country["country_short"]
    #     temp_mongo_id = country["eventId"]
    #     temp_event_id = country["_id"]
    #     if Countries2.objects.filter(name=temp_name).exists():
    #         # Record exists
    #         print("-----------------------Record exists-----------------")
    #     else:
    #         # Record does not exist
    #         print("++++++++++++++++++++++++++++++++Record does not exist++++++++++++++++++++++++")
    #         country_2 = Countries2(
    #         continent = temp_continent,
    #         name = temp_name,
    #         country_code = temp_country_code,
    #         country_short = temp_country_short,
    #         mongo_id = temp_mongo_id,
    #         event_id = temp_event_id,
    #         )
    #         country_2.save()
    # temp_country=Countries2.objects.get(name= 'Italy')
    # print("temp_country =====> ", temp_country)
    cn = 0
    for region in region_data:
            # temp_id = cont_id_dict[country["continent"]][1]
            cn = cn +1
            temp_country=Countries2.objects.get(name= region["country_name"])
            # print("temp_country =====> ", temp_country)
            # if cn == 50:
                # break
            temp_name= region["name"]
            temp_lat_lon = region["lat_lon"]
            temp_lat = region["lat"]
            temp_lon = region["lon"]
            temp_city_code = region["city_code"]
            temp_city_area = region["city_area"]
            temp_mongo_id = region["_id"]
            temp_event_id = region["eventId"]

            if Regions2.objects.filter(name=temp_name).exists():
                # Record exists
                print("-----------------------Record exists-----------------")
            else:
                # Record does not exist
                print("++++++++++++++++++++++++++++++++Record does not exist++++++++++++++++++++++++")
                reg_2 = Regions2(
                    country = temp_country,
                    name =  temp_name.lower(),
                    lat_lon =temp_lat_lon,
                    lat = temp_lat,
                    lon = temp_lon,
                    city_code =temp_city_code,
                    city_area = temp_city_area,
                    mongo_id = temp_mongo_id,
                    event_id = temp_event_id,
                )
                reg_2.save()

    # cont =  Continent.objects.get(mongo_id="62d5ba9647f8b6f7433efefc")
    # cont_id_dict = dict()
    # cont = Continent.objects.all()
    # for i in cont:
    #     print(f"{i.mongo_id} :[{i.name}, {i.id}]")
    #     cont_id_dict[i.mongo_id] = [i.name, i.id]

    # print("country_data[15]", country_data[15])
    # print("cont", cont)
    form = RegionsForm()
    return render(request, 'demos/test_form_2.html', {'form': form, "regionForm":True})
