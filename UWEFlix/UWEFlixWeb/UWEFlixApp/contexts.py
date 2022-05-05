
# A library of functions which return values for view contexts

import datetime
from .models import *

def getDateToday():
    return "%s" % datetime.date.today()

def getAllClubs():
    return Club.objects.all()

def getAllAccounts():
    return Account.objects.all()

def getAllStatements():
    return Statement.objects.all()

def getAllScreens():
    return Screen.objects.all()

def getAllFilms():
    return Film.objects.all()

def getAllShowings():
    return Showing.objects.all()

def getShowingFilms():
    try:
        return Film.objects.filter(id__in=Showing.objects.filter(date=datetime.date.today()).distinct().values_list('film', flat=True))
    except:
        print("here")
        return None

def getUpcomingFilms():
    try:
        return Film.objects.filter(id__in=Showing.objects.filter(date__range=[datetime.date.today().replace(day=datetime.date.today().day + 1), datetime.date.today().replace(month=datetime.date.today().month + 1)]).distinct().values_list('film', flat=True))
    except:
        return None

def getDate(request):
    return request.GET.get('date')

def getAccount(request):
    if request.POST.get('accountID') and not request.POST.get('signinButtonPressed'):
        return Account.objects.get(pk=request.POST.get('accountID'))
    elif request.session.get('_old_post') and request.session.get('_old_post').get('accountID'):
        return Account.objects.get(pk=request.session.get('_old_post').get('accountID'))
    else:
        return None

def getFilm(request):
    return Film.objects.get(pk=request.GET.get('filmID'))

def getShowings(request):
    return Showing.objects.filter(film=Film.objects.get(pk=request.GET.get('filmID')), date=request.GET.get('date'))

def getCost(request):
    cost = request.POST.get('cost')
    if cost:
        return cost
    else:
        account = getAccount(request)
        if account and account.type == "Club Representative":
            return "{:.2f}".format((1 - account.discount / 100) * 6 * int(request.POST.get('noTickets')))
        else:
            return 6 * int(request.POST.get('noTickets'))