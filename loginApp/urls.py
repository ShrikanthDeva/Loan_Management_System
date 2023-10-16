from django.urls import path
from loginApp import views


app_name = 'login_App'
urlpatterns = [
    path('login/', views.login_view, name='login_customer'),
    path('signup/', views.sign_up_view, name='signup_customer'),
    path('logout/', views.logout_view, name='logout'),

]
