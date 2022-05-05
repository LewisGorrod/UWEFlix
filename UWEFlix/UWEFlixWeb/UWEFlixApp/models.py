
from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=20)
    streetNo = models.IntegerField()
    streetName = models.CharField(max_length=20)
    postCode = models.CharField(max_length=7)
    landline = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)
    email = models.CharField(max_length=30)
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=15)
    dob = models.DateField()
    
    def __str__(self):
        return f"{self.name}"

class Account(models.Model):
    fullName = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=20)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    cardNo = models.IntegerField(null=True)
    expiryDate = models.DateField(null=True)
    discount = models.FloatField(null=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.fullName} ({self.type})"

class Statement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    month = models.DateField()

    def __str__(self):
        return f"{self.account} {self.month}"

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    cost = models.FloatField()
    paymentMethod = models.CharField(max_length=6)

    def __str__(self):
        return "{} {} £{:.2f} {}".format(self.account, self.date, self.cost, self.paymentMethod)

class Screen(models.Model):
    number = models.IntegerField()
    noSeats = models.IntegerField()

    def __str__(self):
        return f"Screen {self.number}"

class Film(models.Model):
    title = models.CharField(max_length=30)
    ageRating = models.CharField(max_length=2)
    duration = models.TimeField()
    description = models.CharField(max_length=500)
    poster = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return f"{self.title} ({self.ageRating})"

class Showing(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.time} {self.screen} {self.film}"

class Ticket(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
    type = models.CharField(max_length=7)
    cost = models.IntegerField()
    seatRef = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.id}"
