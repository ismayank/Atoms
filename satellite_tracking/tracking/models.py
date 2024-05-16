from django.db import models

class LaunchCountry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Satellite(models.Model):
    name = models.CharField(max_length=100)
    international_designator = models.CharField(max_length=20)
    norad_id = models.IntegerField()
    launch_date = models.DateField()
    decay_date = models.DateField(null=True, blank=True)
    country = models.ForeignKey(LaunchCountry, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
