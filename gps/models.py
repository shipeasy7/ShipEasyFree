from django.db import models

# Create your models here.
class GPS_status(models.Model):
    mobile_number = models.CharField(max_length=100,null=False, blank=False)
    licen_number = models.CharField(max_length=100, null=False, blank=False)
    # address = models.CharField(max_length=100, null=False, blank=False)
    longitude = models.CharField(max_length=100, null=False, blank=False)
    altitude = models.CharField(max_length=100, null=False, blank=False)
    latitude = models.CharField(max_length=100, null=False, blank=False)
    timestamp = models.CharField(max_length=100, null=False, blank=False)
    driver_name = models.CharField(max_length=100, null=False, blank=False)

    ping_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile_number

class Aproved_mobile_number(models.Model):
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    activation_status = models.BooleanField(default=True)

    def __str__(self):
        return self.mobile_number

class RowData(models.Model):
    mobile_number = models.CharField(max_length=100, null=False, blank=False)
    lat = models.FloatField(max_length=100, null=False, blank=False)
    long = models.FloatField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.mobile_number