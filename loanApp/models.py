from django.db import models
from loginApp.models import CustomerSignUp
import uuid
from dateutil.relativedelta import relativedelta
# Create your models here.


class loanCategory(models.Model):
    loan_name = models.CharField(max_length=250)
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loan_name


class loanRequest(models.Model):
    customer = models.ForeignKey(
        CustomerSignUp, on_delete=models.CASCADE, related_name='loan_customer')
    category = models.ForeignKey(
        loanCategory, on_delete=models.CASCADE, null=True)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending')
    amount = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=1)
    interest_rate = models.FloatField(default=14.0)
    next_due = models.DateField(null=True)
    due_amount = models.PositiveIntegerField(default=0)
    paid_months = models.PositiveIntegerField(default=0)
    paid_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.customer.user.username

    def get_customer_income(self):
        return self.customer.annual_income
    
    def get_customer_credit_score(self):
        return self.customer.credit_score

    def get_loan_category(self):
        return self.category.loan_name
    

    def calculate_emi(self):

        principal = self.amount-self.paid_amount
        years = self.year-(self.paid_months/12)
        # Constants
        months_per_year = 12
        min_interest_earned = 10000

        # Calculate monthly interest rate
        monthly_interest_rate = self.interest_rate / (months_per_year * 100)

        # Calculate total number of payments (EMIs)
        total_payments = years * months_per_year

        # Calculate EMI
        emi = principal * monthly_interest_rate * ((1 + monthly_interest_rate) ** total_payments) /(((1 + monthly_interest_rate) ** total_payments) - 1)

        # Calculate total interest earned by the bank
        total_interest_earned = (emi * total_payments) - principal

        # Check if the interest rate is below the limit
        while total_interest_earned <= min_interest_earned:
            # If the total interest earned is not sufficient, increase the interest rate
            self.interest_rate += 0.1  # You can adjust the increment as needed
            monthly_interest_rate = self.interest_rate / (months_per_year * 100)

            # Recalculate EMI and total interest earned
            emi = principal * monthly_interest_rate * ((1 + monthly_interest_rate) ** total_payments) / \
                  (((1 + monthly_interest_rate) ** total_payments) - 1)
            total_interest_earned = (emi * total_payments) - principal

        # Update the EMI details
        self.due_amount = emi
        if self.next_due is None:
            self.next_due = self.request_date + relativedelta(months=1)
            self.next_due = self.next_due.replace(day=1)
        else:
            self.update_due_date()
        self.save()

    def update_due_date(self):
        # Calculate the next month of the next_due date
        next_month = self.next_due + relativedelta(months=1)
        
        # Set the next_due date to the 1st day of the next month
        self.next_due = next_month.replace(day=1)
        self.save()

    def pay_emi(self,amount):
        self.paid_amount += amount
        self.paid_months += 1
        self.calculate_emi()

    def isPaid(self):

        date1_value = self.request_date
        date2_value = self.next_due

        # Calculate the difference in months using relativedelta
        difference = relativedelta(date1_value, date2_value)

        # Calculate the total number of months
        months = difference.years * 12 + difference.months

        if months != 0:
            return True

        return False


class loanTransaction(models.Model):
    customer = models.ForeignKey(
        CustomerSignUp, on_delete=models.CASCADE, related_name='transaction_customer')
    loan = models.PositiveIntegerField(default=0)
    transaction = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.username
