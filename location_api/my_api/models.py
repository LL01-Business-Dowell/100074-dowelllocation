from django.db import models

# Create your models here.
# Create your models here.
class Continent(models.Model):
    name = models.CharField(max_length=300)
    mongo_id = models.CharField(max_length=300, default="CONTINENTMONGOID")
    event_id = models.CharField(max_length=300, default="EVENTMONGOID")
    def __str__(self):
        return self.name
    @classmethod
    def get_default_pk(cls):
        continent, created = cls.objects.get_or_create(
            name='default continent')# defaults=dict(description='this is not an exam'))
        return continent.pk


    class Meta:
        ordering = ['name']
class Countries(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, default=Continent.get_default_pk)
    name = models.CharField(max_length=300)
    country_code = models.CharField(max_length=5,default="000")
    country_short = models.CharField(max_length=6, default="IIII")
    mongo_id = models.CharField(max_length=300, default="COUNTRYMONGOID")
    event_id = models.CharField(max_length=300, default="EVENTMONGOID")


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Regions(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name =  models.CharField(max_length=300)
    lat_lon = models.CharField(max_length=600,  default="DefaultName")
    city_code = models.CharField(max_length=25, default="CITY")
    city_area = models.CharField(max_length=25, default="000")
    mongo_id = models.CharField(max_length=300, default="REGIONMONGOID")
    event_id = models.CharField(max_length=300, default="EVENTMONGOID")


    def __str__(self):
        return str(self.name)
class RequestsRec(models.Model):
    req =  models.TextField(default  ="Default")
    url_req = models.TextField(default= "Default")
    response = models.TextField(default = "Default")
    username = models.TextField(default="Default")
    session_id = models.TextField(default="Default")
    date_time_rec = models.CharField(max_length = 500, default="None")
    mongo_id = models.CharField(max_length=300, default="REQMONGOID")
    event_id = models.CharField(max_length=300, default="REQEVENTID")
    time_z = models.CharField(max_length=300, default='Africa/Abidjan')
    project_code = models.CharField(max_length=300, default='None')
    is_success = models.BooleanField(default=False)
    is_error = models.BooleanField(default = True)
    def __str__(self):
        return str(self.username)
class SubRegions(models.Model):
    regions = models.ForeignKey(Regions, on_delete=models.CASCADE)
    name =  models.CharField(max_length=300)
    mongo_id = models.CharField(max_length=300, default="SUBREGIONMONGOID")
    event_id = models.CharField(max_length=300, default="EVENTMONGOID")


    def __str__(self):
        return self.name
class TimeZoneDb(models.Model):
    utc_attained = models.CharField(max_length=300)
    timezone_attained = models.CharField(max_length=300)
    country_attained = models.CharField(max_length=300)
    city_attained = models.CharField(max_length=300)

    def __str__(self):
        return self.city_attained+ self.utc_attained
