from django.contrib import admin
from .models import loanRequest, loanCategory, loanTransaction
# Register your models here.loanCategory,
admin.site.register(loanRequest)
admin.site.register(loanCategory)
admin.site.register(loanTransaction)
