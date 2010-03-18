from django.db import models

class MyModel(models.Model):
    name  = models.CharField(max_length=25)
    color = models.CharField(max_length=20)
    price = models.IntegerField(default=100)

    def __unicode__(self):
        return self.name
