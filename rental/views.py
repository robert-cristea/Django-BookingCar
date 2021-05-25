import dateutil.parser

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
# Create your views here.
from rental.models import Booking, Car


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'registration/login.html'
    template_name = 'rental/index.html'
    model = Car
    context_object_name = "list"

    def get_queryset(self):
        c = Car.objects.all()
        return c



# class ViewCar(LoginRequiredMixin, generic.DetailView):
#     login_url = 'registration/login.html'
#     template_name = 'rental/viewCar.html'
#     model = Car



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
        print('===========================')
        print(request.user.id)
        print('===========================')
        carId = request.POST['carId']
        carObj = Car.objects.get(id=carId)
        startDate = request.POST['start-date']
        endDate = request.POST['end-date']

        # booking = Booking.objects.get(carID = carObj)

        try:
            booking = Booking.objects.get(carID = carObj)
            prevEndDate = booking.endDate
            if prevEndDate > dateutil.parser.parse(startDate).date():
                # print('Cannot book')
                context = {'car':carObj, 'message':'Failure in booking!', 'state':0}
            else:
                booking = Booking()
                booking.carID = carObj
                booking.startDate = startDate
                booking.endDate = endDate
                booking.user = User.objects.get(id=request.user.id)
                booking.save()
                context = {'car':carObj, 'message':'Succeed in booking!', 'state':1}

        except Booking.DoesNotExist:
            booking = Booking()
            booking.carID = carObj
            booking.startDate = startDate
            booking.endDate = endDate
            booking.user = User.objects.get(id=request.user.id)
            booking.save()

            context = {'car':carObj, 'message':'Succeed in booking!', 'state':1}

        return render(request, 'rental/viewCar.html', context)
    # try:
    #     for k, v in request.GET.items():
    #         if k != "csrfmiddlewaretoken":
    #             car_id = k
    #     car = Car.objects.get(id=car_id)
    #     context = {'car': car}
    # except Car.DoesNotExist:
    #     raise Http404("Car not found")
    # return render(request, "rental/viewCar.html")
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def loginVerify(request):
    uname = request.POST['uname']
    passw = request.POST['passw']
    u = authenticate(request, username=uname, password=passw)
    if u is not None:
        login(request, u)
        return HttpResponseRedirect(reverse('rental:index'))
    else:
        return HttpResponseRedirect('/accounts/login')
