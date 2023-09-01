from django import forms
from .models import Continent, Countries,Regions, SubRegions
bad_continents = ["default continent", "dummy_continent"]
bad_country_id_list = [14,8,9,11,13,10,63, 64,16, 15, 46, 78]
bad_country_name_list = ["China_Error",
"dummy_country","dummy_country2","Indonesia_Error",
"Indonesia_Error","Myanmar_Error","Singapore_Error",
"Dummy Country", "Dummy Country 2",
"Dummy Country 3", "Document 12"]
bad_region_id_list = [1,2]
bad_name_list = ["dummy_region","dummy_region_22", "Bangalore", "Dummy City"]
class ContinentForm(forms.ModelForm):
    class Meta:
        model = Continent
        fields = ['name']  # List the fields you want in the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # excluded_authors = Countries.objects.all(name__icontains='excluded')
        # .exclude(id__in=bad_id_list)
        # Add CSS classes to fields
        self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter continent name'})
class CountriesForm(forms.ModelForm):
    class Meta:
        model = Countries
        fields = ["continent","name","country_code","country_short",]  # List the fields you want in the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # excluded_authors = Countries.objects.all(name__icontains='excluded')
        # .exclude(id__in=bad_id_list)
        # Add CSS classes to fields
        self.fields['continent'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter country name'})
        self.fields['country_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['country_short'].widget.attrs.update({'class': 'form-control'})
        # self.fields['author'].widget.attrs.update({'class': 'custom-author-class'})
        self.fields['continent'].queryset =  Continent.objects.all().exclude(name__in=bad_continents)

class RegionsForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = ["country","name","lat_lon","city_code","city_area"]  # List the fields you want in the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # excluded_authors = Countries.objects.all(name__icontains='excluded')
        # .exclude(id__in=bad_id_list)
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter city name'})
        # self.fields['lat_lon'].widget.attrs['default'] = ''
        # self.fields['lat_lon'].widget.attrs.pop('default',None)
        # self.fields['lat_lon'].widget.attrs.update(d= '')
        self.fields['lat_lon'].initial = ''
        self.fields['lat_lon'].widget.attrs.update({'class': 'form-control', 'value':'','placeholder':'eg. \"51.507351 °N 0.127758 °W\"'})
        self.fields['city_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['city_area'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].queryset =  Countries.objects.all().exclude(id__in=bad_country_id_list).exclude(name__in=bad_country_name_list)
class SubRegionsForm(forms.ModelForm):
    class Meta:
        model = SubRegions
        fields = ["regions","name"]   # List the fields you want in the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # excluded_authors = Countries.objects.all(name__icontains='excluded')
        # .exclude(id__in=bad_id_list)
        self.fields['regions'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter area name'})
        self.fields['regions'].queryset = Regions.objects.all().exclude(id__in=bad_region_id_list).exclude(name__in=bad_name_list).order_by('name')