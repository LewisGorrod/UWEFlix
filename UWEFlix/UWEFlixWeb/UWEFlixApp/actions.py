
# A library of functions which handle form actions

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .contexts import getCost

# Database actions

def addClub(request):
    name = request.POST.get('name')
    streetNo = int(request.POST.get('streetNo'))
    streetName = request.POST.get('streetName')
    postCode = request.POST.get('postCode')
    landline = request.POST.get('landline')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    firstName = request.POST.get('firstName')
    lastName = request.POST.get('lastName')
    dob = request.POST.get('dob')
    club = Club(name=name, streetNo=streetNo, streetName=streetName, postCode=postCode, landline=landline, mobile=mobile, email=email, firstName=firstName, lastName=lastName, dob=dob)
    club.save()

def deleteClub(request):
    clubID = request.POST.get('clubID')
    club = Club.objects.get(pk=clubID)
    club.delete()

def addAccount(request):
    fullName = request.POST.get('fullName')
    clubID = request.POST.get('clubID')
    if clubID != "None":
        club = Club.objects.get(pk=clubID)
    else:
        club = None
    type = request.POST.get('type')
    cardNo = request.POST.get('cardNo')
    expiryDate = request.POST.get('expiryDate')
    discount = request.POST.get('discount')
    password = request.POST.get('password')
    account = Account(fullName=fullName, club=club, type=type, cardNo=cardNo, expiryDate=expiryDate, discount=discount, password=password)
    account.save()

def deleteAccount(request):
    accountID = request.POST.get('accountID')
    account = Account.ojects.get(pk=accountID)
    account.delete()

def addScreen(request):
    number = request.POST.get('number')
    noSeats = request.POST.get('noSeats')
    screen = Screen(number=number, noSeats=noSeats)
    screen.save()

def deleteScreen(request):
    screenID = request.POST.get('screenID')
    screen = Screen.objects.get(pk=screenID)
    screen.delete()

def addFilm(request):
    title = request.POST.get('title')
    ageRating = request.POST.get('ageRating')
    duration = request.POST.get('duration')
    description = request.POST.get('description')
    film = Film(title=title, ageRating=ageRating, duration=duration, description=description)
    film.save()

def deleteFilm(request):
    filmID = request.POST.get('filmID')
    film = Film.objects.get(pk=filmID)
    film.delete()

def addShowing(request):
    screenID = request.POST.get('screenID')
    filmID = request.POST.get('filmID')
    date = request.POST.get('date')
    time = request.POST.get('time')
    screen = Screen.objects.get(pk=screenID)
    film = Film.objects.get(pk=filmID)
    showing = Showing(screen=screen, film=film, date=date, time=time)
    showing.save()

def deleteShowing(request):
    showingID = request.POST.get('showingID')
    showing = Showing.objects.get(pk=showingID)
    showing.delete()

# Popups (only change the content of a template)

def signinPopup(request, context):
    context['signinButtonPressed'] = True

def paymentPopup(request, context):
    context['paymentButtonPressed'] = True
    context['cost'] = getCost(request)

def bookingPopup(request, context):
    context['bookingButtonPressed'] = True

# Links (may also render a different template)

def signin(request, context):
    if request.POST.get('accountID'):
        try:
            account = Account.objects.get(pk=request.POST.get('accountID'))
            if request.POST.get('accountType') == account.type and request.POST.get('accountPassword') == account.password:
                context['account'] = account
                request.session['_old_post'] = request.POST
                if account.type == "Club Representative":
                    context['signinButtonPressed'] = False
                    return render(request, f"UWEFlixApp/visitor{request.path[:-1]}.html", context)
                elif account.type == "Accounts Department":
                    return redirect(reverse('accounts'))
                elif account.type == "Cinema Manager":
                    return redirect(reverse('manager'))
            else:
                context['signinFailed'] = True
                return render(request, f"UWEFlixApp/visitor{request.path[:-1]}.html", context)
        except:
            context['signinFailed'] = True
            return render(request, f"UWEFlixApp/visitor{request.path[:-1]}.html", context)
    else:
        context['signinFailed'] = True
        return render(request, f"UWEFlixApp/visitor{request.path[:-1]}.html", context)

def signout(request, context):
    context['account'] = None
    request.session['_old_post'] = None
    return redirect(reverse('home'))

def payment(request, context):
    context['paymentButtonPressed'] = True
    context['cost'] = getCost(request)
    context['cardNoInvalid'] = not validateCardNo(request.POST.get('cardNo'))
    context['cvvInvalid'] = not validateCVV(request.POST.get('cvv'))
    context['expiryDateInvalid'] = not validateExpiryDate(request.POST.get('expiryDate'))
    context['cardNameInvalid'] = not validateCardName(request.POST.get('cardName'))
    context['cardExpired'] = isCardExpired(request.POST.get('expiryDate'))

def booking(request):
    showingID = request.POST.get('showingID')
    noTickets = request.POST.get('noTickets')
    cost = request.POST.get('cost')
    showing = Showing.objects.get(pk=showingID)
    film = showing.film
    date = showing.date
    time = showing.time
    paymentMethod = "TFR"
    account = request.POST.get('account')
    if account == None:
        statement = None
    else:
        statement = Statement.objects.get(account=account)
    transaction = Transaction(account=account, statement=statement, date=date, cost=cost, paymentMethod=paymentMethod)
    transaction.save()
    return render(request, 'UWEFlixApp/visitor/booking.html', {'bookingID': transaction.id, 'film': film, 'date': date, 'time': time, 'noTickets': noTickets})

def viewStatement(request, context):
    context['viewStatement'] = True
    context['statement'] = Statement.objects.get(pk=request.POST.get('statementID'))
    context['statementAccount'] = Account.objects.get(pk=context['statement'].account.id)
    context['transactions'] = Transaction.objects.filter(account=context['statementAccount'])

# Validation functions

def validatePayment(request):
    None

def validateCardNo(cardNo):
    if len(cardNo) == 16:
        try:
            sum = 0
            for d in range(16):
                tmp = int(cardNo[d])
                if d % 2 == 0:
                    tmp *= 2
                    if tmp > 9:
                        tmp -= 9
                sum += tmp
            if sum % 10 == 0:
                return True
            else:
                return False
        except:
            return False
    else:
        return False

def validateCVV(cvv):
    if len(cvv) == 3:
        try:
            int(cvv)
            return True
        except:
            return False
    else:
        return False

def validateExpiryDate(expiryDate):
    if len(expiryDate) == 5:
        try:
            int(expiryDate[0:2])
            if expiryDate[2] != '/':
                return False
            int(expiryDate[4:6])
            return True
        except:
            return False
    else:
        return False

def validateCardName(cardName):
    if len(cardName) > 0:
        return True
    else:
        return False

def isCardExpired(expiryDate):
    return False # Leave for now