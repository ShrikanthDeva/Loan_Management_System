from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

class CustomerSignUp(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='customer')
    aadhar_id = models.CharField(max_length=50, unique=True,default=None)
    annual_income = models.PositiveIntegerField(blank=True, null=True)
    credit_score = models.PositiveIntegerField(default=300, validators=[MaxValueValidator(900), MinValueValidator(300)])

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    TRANSACTION_TYPES = (('CREDIT', 'Credit'),('DEBIT', 'Debit'),)

    aadhar_id = models.CharField(max_length=50,default=None)
    date = models.DateField()
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.amount} on {self.date} for User: {self.user.username}"
