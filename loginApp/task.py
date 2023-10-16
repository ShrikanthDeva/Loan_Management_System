import csv
from .models import Transaction, CustomerSignUp
from django.db.models import Sum

def calculate_credit_score(aadhar_id):
    user = CustomerSignUp.objects.get(aadhar_id=aadhar_id)
    if Transaction.objects.count() == 0:
        print("IMPORTING TRANSACTIONS")
        import_transactions()
    else:
        print("Already Imported")
    

    credit_total = Transaction.objects.filter(aadhar_id=aadhar_id,transaction_type='CREDIT').aggregate(credit_total=Sum('amount'))['credit_total']
    debit_total = Transaction.objects.filter(aadhar_id=aadhar_id,transaction_type='DEBIT').aggregate(debit_total=Sum('amount'))['debit_total']
    total_balance = -(credit_total-debit_total)

    print(total_balance,total_balance >= 1000000,total_balance <= 10000 )
    if total_balance >= 1000000:
        user.credit_score = 900
    elif total_balance <= 10000:
        user.credit_score = 300
    else:
        # Calculate change in account balance
        balance_change = total_balance - 10000  # Assuming the lower bound is 100,000

        # Credit score changes by 10 points for every Rs. 15,000 change in balance
        credit_score_change = balance_change // 15000 * 10
        print(credit_score_change)
        user.credit_score = 300 + credit_score_change

    user.save()


def import_transactions():

    with open('transactions_data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            aadhar_id = row['user']
            date = row['date']
            transaction_type = row['transaction_type']
            amount = float(row['amount'])
            transac = Transaction(aadhar_id=aadhar_id,date=date,transaction_type=transaction_type,amount=amount)
            transac.save()