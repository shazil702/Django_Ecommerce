from django.db import models
from django.conf import settings

# Create your models here.
class Adress(models.Model):
    adress_id = models.AutoField(primary_key=True)
    adress_name = models.CharField(max_length=250)
    adress_lastname = models.CharField(max_length=250, blank=True)
    adress_state = models.CharField(max_length=100)
    adress_house = models.TextField()
    adress_area = models.TextField()
    adress_city = models.CharField(max_length=200)
    adress_phone = models.CharField(max_length=200)
    adress_pincode = models.IntegerField()
    adress_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.adress_name + " " + self.adress_lastname
    
    class Meta:
        unique_together = ('adress_phone', 'adress_pincode', 'adress_user')
