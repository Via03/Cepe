from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Skill, Booking

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Booking)