import dateutil.parser

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
# Create your views here.
from rental.models import Booking, Car
from accounts.models import Profile

from dateutil.parser import parse


@login_required
def index(request):
    cars = Car.objects.all()
    context = {'list':cars}

    return render(request, "rental/index.html", context)

def viewCar(request):
    try:
        for k, v in request.GET.items():
            if k != "csrfmiddlewaretoken":
                car_id = k
        car = Car.objects.get(id=car_id)
        context = {'car': car}
    except Car.DoesNotExist:
        raise Http404("Car not found")
    return render(request, "rental/viewCar.html", context)

def bookCar(request):
    if request.method == "POST":
        carId = request.POST['carId']
        carObj = Car.objects.get(id=carId)
        
        startDate = request.POST['start-date']
        endDate = request.POST['end-date']



        if startDate == "" or endDate == "":
            context = {'car':carObj, 'message':'Please fill in the blanks!', 'state':0}
            return render(request, 'rental/viewCar.html', context)
        elif parse(startDate) > parse(endDate):
            context = {'car':carObj, 'message':'Start Date must be smaller than End Date!', 'state':0}
            return render(request, 'rental/viewCar.html', context)
            
        booking = Booking.objects.filter(carID = carObj).order_by('-startDate').first()
        if booking is not None:
            prevEndDate = booking.endDate
            if prevEndDate >= dateutil.parser.parse(startDate).date():
                context = {'car':carObj, 'message':'Failure! This car has been already booked.', 'state':0}
            else:
                booking = Booking()
                booking.carID = carObj
                booking.startDate = startDate
                booking.endDate = endDate
                booking.user = User.objects.get(id=request.user.id)
                booking.save()
                context = {'car':carObj, 'message':'Success! You have booked this car.', 'state':1}

        else:
            booking = Booking()
            booking.carID = carObj
            booking.startDate = startDate
            booking.endDate = endDate
            booking.user = User.objects.get(id=request.user.id)
            booking.save()

            context = {'car':carObj, 'message':'Success! You have booked this car.', 'state':1}

        return render(request, 'rental/viewCar.html', context)

