
# Functions which are not returned by views only change the content of templates.
# Functions which are returned by views may render another template at a new url.

from .models import *
from .contexts import *
from .actions import *
from .forms import FilmForm

def home(request):
    context = {
        'account': getAccount(request),
        'date': getDateToday(),
        'showingFilms': getShowingFilms(),
        'upcomingFilms': getUpcomingFilms(),
    }
    if request.POST.get('signinButtonPressed'):
        signinPopup(request, context)
    if request.POST.get('signin'):
        return signin(request, context)
    if request.POST.get('signoutButtonPressed'):
        return signout(request, context)
    return render(request, 'UWEFlixApp/visitor/home.html', context)

def film(request):
    context = {
        'account': getAccount(request),
        'date': getDate(request),
        'film': getFilm(request),
        'showings': getShowings(request),
    }
    if request.POST.get('signinButtonPressed'):
        signinPopup(request, context)
    if request.POST.get('signin'):
        return signin(request, context)
    if request.POST.get('signoutButtonPressed'):
        return signout(request, context)
    if request.POST.get('paymentButtonPressed'):
        paymentPopup(request, context)
    if request.POST.get('payment'):
        payment(request, context)
    return render(request, 'UWEFlixApp/visitor/film.html', context)

def accounts(request):
    context = {
        'account': getAccount(request),
        'clubs': getAllClubs(),
        'accounts': getAllAccounts(),
        'statements': getAllStatements(),
    }
    if request.POST.get('signoutButtonPressed'):
        return signout(request, context)
    if request.POST.get('addAccount'):
        addAccount(request)
    if request.POST.get('deleteAccount'):
        deleteAccount(request)
    if request.POST.get('viewStatement'):
        viewStatement(request, context)
    return render(request, 'UWEFlixApp/admin/accounts.html', context)

def manager(request):
    context = {
        'account': getAccount(request),
        'clubs': getAllClubs(),
        'screens': getAllScreens(),
        'films': getAllFilms(),
        'showings': getAllShowings(),
    }
    if request.POST.get('signoutButtonPressed'):
        return signout(request, context)
    if request.POST.get('addClub'):
        addClub(request)
    if request.POST.get('deleteClub'):
        deleteClub(request)
    if request.POST.get('addScreen'):
        addScreen(request)
    if request.POST.get('deleteScreen'):
        deleteScreen(request)
    if request.POST.get('addFilm'):
        addFilm(request)
    if request.POST.get('deleteFilm'):
        deleteFilm(request)
    if request.POST.get('addShowing'):
        addShowing(request)
    if request.POST.get('deleteShowing'):
        deleteShowing(request)
    # Image upload
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = FilmForm()
    context['form'] = form
    return render(request, 'UWEFlixApp/admin/manager.html', context)