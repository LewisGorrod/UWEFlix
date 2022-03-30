from django.db import models

class ClubReg(models.Model):
    clubID = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    streetNo = models.IntegerField(default=0)
    streetName = models.CharField(max_length=200)
    postCode = models.CharField(max_length=200)
    landline = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    dob = models.DateField('Date of birth')
    
    def __str__(self):
        return f"{self.clubID}, {self.name}, {self.streetNo}, {self.streetName}, {self.postCode}, {self.landline}, {self.mobile}, {self.email}, {self.firstName}, {self.lastName}, {self.dob}"

class Account(models.Model):
    accountID = models.IntegerField(default=0)
    clubID = models.ForeignKey(ClubReg, on_delete=models.CASCADE)
    cardNo = models.IntegerField(default=0)
    expiryDate = models.DateField('Expiry date')
    discount = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.accountID}, {self.clubID}, {self.cardNo}, {self.expiryDate}, {self.discount}"

class EndOfMonthStatement(models.Model):
    statementID = models.IntegerField(default=0)
    accountID = models.ForeignKey(Account, on_delete=models.CASCADE)
    month = models.DateField('Month')

    def __str__(self):
        return f"{self.statementID}, {self.accountID}, {self.month}"

class Transaction(models.Model):
    transactionID = models.IntegerField(default=0)
    accountID = models.ForeignKey(Account, on_delete=models.CASCADE)
    purchaseDateTime = models.DateTimeField('Purchase date/time')
    noTickets = models.IntegerField(default=0)
    cost = models.FloatField(default=0.0)
    paymentType = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.transactionID}, {self.accountID}, {self.purchaseDateTime}, {self.noTickets}, {self.cost}, {self.paymentType}"

class Screen(models.Model):
    screenID = models.IntegerField(default=0)
    screenNo = models.IntegerField(default=0)
    noSeats = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.screenID}, {self.screenNo}, {self.noSeats}"

class Film(models.Model):
    filmID = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    ageRating = models.CharField(max_length=100)
    duration = models.DateTimeField('Duration')
    trailerDescription = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.filmID}, {self.title}, {self.ageRating}, {self.duration}, {self.trailerDescription}"

class Showing(models.Model):
    showingID = models.IntegerField(default=0)
    screenID = models.ForeignKey(Screen, on_delete=models.CASCADE)
    filmID = models.ForeignKey(Film, on_delete=models.CASCADE)
    dateTime = models.DateTimeField('Showing date/time')

    def __str__(self):
        return f"{self.showingID}, {self.screenID}, {self.filmID}, {self.dateTime}"

class Ticket(models.Model):
    ticketID = models.IntegerField(default=0)
    showingID = models.ForeignKey(Showing, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    cost = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.ticketID}, {self.showingID}, {self.type}, {self.cost}"
