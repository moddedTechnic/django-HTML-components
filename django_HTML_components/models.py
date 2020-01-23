from django.db import models

# Create your models here.
class ProductModel(models.Model):
    name = models.CharField(max_length=128)
    desc = models.CharField(max_length=1024)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
