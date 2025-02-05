from django.db import models

# Create your models here.
class Pays(models.Model):
    pays_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)


    def __str__(self):
        return self.name