from django.contrib import admin

# Register your models here.
from rental.models import Car, User, Booking

admin.site.register(Car)
#admin.site.register(User)
admin.site.register(Booking)
