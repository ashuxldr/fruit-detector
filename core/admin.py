from django.contrib import admin
from .models import Fruit, Session, Alert
# Register your models here.
admin.site.register(Fruit)
admin.site.register(Session)
admin.site.register(Alert)