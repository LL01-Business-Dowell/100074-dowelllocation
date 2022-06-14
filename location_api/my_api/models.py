from django.db import models

# Create your models here.
class Countries(models.Model):
    name = models.CharField(max_length=300)
    country_code = models.CharField(max_length=5,default="000")
    country_short = models.CharField(max_length=6, default="IIII")
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
    
class Regions(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name =  models.CharField(max_length=300)
    def __str__(self):
        return str(self.name)
class SubRegions(models.Model):
    regions = models.ForeignKey(Regions, on_delete=models.CASCADE)
    name =  models.CharField(max_length=300)
    def __str__(self):
        return self.name
