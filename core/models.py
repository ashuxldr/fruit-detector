from django.db import models
from datetime import date

class Fruit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    calorie = models.DecimalField(max_digits=10, decimal_places=2)
    carbohydrate = models.DecimalField(max_digits=10, decimal_places=2)
    protein = models.DecimalField(max_digits=10, decimal_places=2)
    fat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=250)
    total_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    total_carbohydrate = models.DecimalField(max_digits=10, decimal_places=2)
    total_protein = models.DecimalField(max_digits=10, decimal_places=2)
    total_fat = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today())


class Alert(models.Model):
    alert_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    alert_carbohydrate = models.DecimalField(max_digits=10, decimal_places=2)
    alert_protein = models.DecimalField(max_digits=10, decimal_places=2)
    alert_fat = models.DecimalField(max_digits=10, decimal_places=2)



