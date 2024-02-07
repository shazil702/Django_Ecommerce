from django.db import models

# Create your models here.
class Intent(models.Model):
    name = models.CharField(max_length=300)
    keyword = models.TextField()

    def __str__(self):
        return self.name
    
class Entities(models.Model):
    name = models.CharField(max_length=300)
    value = models.TextField()
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    text = models.TextField()
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    entities = models.ManyToManyField(Entities, blank=True)
    
    def __str__(self):
        return self.text[0:30]
