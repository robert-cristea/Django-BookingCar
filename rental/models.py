from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
# Create your models here.


class Car(models.Model):
    carName = models.CharField(max_length=30)
    priceDay = models.FloatField()
    priceWeek = models.FloatField()
    numSeats = models.IntegerField()
    numDoors = models.IntegerField()
    # brand = models.CharField(max_length=20)
    # model = models.CharField(max_length=20)
    gear = models.CharField(max_length=9)

    def __str__(self):
        return self.carName


class Booking(models.Model):
    carID = models.ForeignKey(Car, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Booking #" + self.bookingID


class UserType(models.Model):
    userType = models.IntegerField()
    typeDesc = models.CharField(max_length=5)



# class User(models.Model):
#     username = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)
#     firstName = models.CharField(max_length=20)
#     lastName = models.CharField(max_length=30)
#     email = models.CharField(max_length=30)
#     phoneNumber = models.CharField(max_length=10)
#     usertype = models.ForeignKey(UserType, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.firstName + " " + self.lastName





