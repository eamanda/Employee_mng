from django.urls import path
from employee.views import *

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('auth_employee_add',auth_employee_add,name='auth_employee_add'),
    path('<int:id>/details/', employee_details, name='employee_details'),
    path('<int:id>/edit/', employee_edit, name='employee_edit'),
    path('add/', employee_add, name='employee_add'),
    path('<int:id>/delete/', employee_delete, name='employee_delete'),
    path('profile/update/', ProfileUpdate.as_view(), name='update_profile'),
]
