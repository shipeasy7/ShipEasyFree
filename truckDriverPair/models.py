from django.db import models
from truck.models import Truck_data
from driver.models import Driver_add
# Create your models here.
class Pair_and_status(models.Model):
    truck = models.ForeignKey(Truck_data, on_delete=models.PROTECT, null = True, blank = True,related_name="%(app_label)s_%(class)s_related")
    driver = models.ForeignKey(Driver_add, on_delete=models.PROTECT, null = True, blank = True,related_name="%(app_label)s_%(class)s_related")

    empty_status = models.BooleanField(default=False)
    maintaion_status = models.BooleanField(default=False)
    break_down_status = models.BooleanField(default=False)
    shipment_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Shipment_ids(models.Model):
    pair_id = models.ForeignKey(Pair_and_status,on_delete=models.PROTECT, null = True, blank = True,related_name="%(app_label)s_%(class)s_related")
    shipment_id = models.CharField(max_length=100,null=False, blank=False)
    ship_form = models.CharField(max_length=100,null=True, blank=False)
    ship_to = models.CharField(max_length=100,null=True, blank=False)
    name_of_customer = models.CharField(max_length=100,null=True, blank=False)
    contact = models.CharField(max_length=100,null=True, blank=False)
    invoice_id = models.CharField(max_length=100,null=True, blank=False)
    start_shipment = models.DateTimeField(auto_now = True)
    end_shipment = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.pair_id