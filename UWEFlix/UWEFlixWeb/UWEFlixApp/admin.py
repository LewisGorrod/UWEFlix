from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Club)
admin.site.register(Account)
admin.site.register(Statement)
admin.site.register(Transaction)
admin.site.register(Screen)
admin.site.register(Film)
admin.site.register(Showing)
admin.site.register(Ticket)