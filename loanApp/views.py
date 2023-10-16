from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoanRequestForm, LoanTransactionForm
from .models import loanRequest, loanTransaction
# Create your views here.



def home(request):
    return render(request, 'home.html', context={})


@login_required(login_url='/account/login-customer')
def LoanRequest(request):

    error = ''
    form = LoanRequestForm()

    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        max_loans = {'Home Loan': 8500000, 'Car Loan': 750000, 'Personal Loan': 1000000, 'Educational Loan': 5000000}
        if form.is_valid():
            loan_obj = form.save(commit=False)
            loan_obj.customer = request.user.customer
            category = loan_obj.get_loan_category()
            amount = loan_obj.amount
            if 0 < amount <= max_loans[category]  :
                # perfrom income and creditscore check
                customer_income = loan_obj.get_customer_income()
                customer_credit_score = loan_obj.get_customer_credit_score()
                print(customer_income, customer_credit_score )
                if customer_credit_score >= 450 and customer_income >= 150000:
                    # perfrom emi checks
                    # return emi dates
                    loan_obj.status = 'Accepted'
                    loan_obj.save()
                    loan_obj.calculate_emi()
                    loan_details = loans = loanRequest.objects.filter(id = loan_obj.id)
                    print(loan_details)
                    # redirect to page stating the loan id and details of emi
                    return render(request, 'loanApp/loanresult.html', context={'form': form, 'error': error,'loans': loan_details})
                else:
                    loan_obj.status = 'Rejected'
                    loan_obj.save()
                    error = "You Can't Avail Loan as your credit_score (or) Income is low :("
                    return render(request, 'loanApp/loanresult.html', context={'form': form, 'error': error})
                
            else:
                error = f'Maximum Permissible Amount for {category} is {max_loans[category]} !'


    return render(request, 'loanApp/loanrequest.html', context={'form': form, 'error': error})

@login_required(login_url='/account/login-customer')
def LoanPayment(request):
    error = ''
    form = LoanTransactionForm()
    if request.method == 'POST':
        form = LoanTransactionForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user.customer
            loan_id = payment.loan
            customer_loan = loanRequest.objects.filter(
                    customer=request.user.customer,id=loan_id)
            if customer_loan.count() == 0:
                error = 'Invalid Loan ID'
                return render(request, 'loanApp/payment.html', context={'form': form, 'error': error})
            else:
                if customer_loan[0].isPaid():
                    error = 'EMI paid for this month'
                    return render(request, 'loanApp/payment.html', context={'form': form, 'error': error})
                else:
                    payment.save()
                    print(customer_loan[0].customer_id,customer_loan[0].id,customer_loan[0].amount)
                    customer_loan[0].pay_emi(amount=payment.payment)
            
                    return UserLoanHistory(request=request)
        # print(form.data)
    return render(request, 'loanApp/payment.html', context={'form': form, 'error': error})


@login_required(login_url='/account/login-customer')
def UserTransaction(request):
    transactions = loanTransaction.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_transaction.html', context={'transactions': transactions})


@login_required(login_url='/account/login-customer')
def UserLoanHistory(request):
    loans = loanRequest.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_loan_history.html', context={'loans': loans})



def error_404_view(request, exception):
    print("not found")
    return render(request, 'notFound.html')
