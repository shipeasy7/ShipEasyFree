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

    def __str__(self):
        return str(self.id)