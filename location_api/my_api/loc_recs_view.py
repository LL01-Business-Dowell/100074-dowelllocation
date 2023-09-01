from django.shortcuts import render, redirect
from .forms import ContinentForm ,CountriesForm, RegionsForm, SubRegionsForm
from django.http import Http404, JsonResponse
from my_api.models import Countries, Regions, SubRegions, Continent, RequestsRec
from .foreign_data import country_mapper, continent_mapper, write_locs, read_locs, del_locs, mongo_create, continent_name_mapper, get_event_id
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
            return render(request, 'demos/form_template.html.html', {'form': form, "success":True, "regionForm":True})
            # else:
                # return render(request, 'demos/form_template.html', {'form': form, "error":True, "message":"Error occured during entry of city","regionForm":True})

        else:
            form = RegionsForm()
            return render(request, 'demos/form_template.html.html', {'form': form, "error":True, "message":"City exists already","regionForm":True})
    else:
        form = RegionsForm()

    return render(request, 'demos/form_template.html', {'form': form, "regionForm":True})

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
    form = RegionsForm()
    return render(request, 'demos/test_form_2.html', {'form': form, "regionForm":True})
