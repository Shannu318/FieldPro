"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('', user_views.user_login, name='home'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('customer/profile/', user_views.customer_profile, name='customer_profile'),
    path('customer/service-request/create/',user_views.create_service_request,
         name='create_service_request'
         ),
    path('customer/service-requests/', user_views.my_service_requests,
          name='my_service_requests'
          ),
    path('customer/service-requests/<int:service_request_id>/', 
         user_views.service_request_detail,
         name='service_request_detail'
         ),
    path(
        'customer/service-requests/<int:service_request_id>/cancel/',
        user_views.cancel_service_request,
        name='cancel_service_request'
        ),
    path('technician/dashboard/', user_views.technician_dashboard,
         name='technician_dashboard'
         ),
    path('technician/service-requests/<int:request_id>/',
         user_views.technician_service_request_detail,
         name='technician_service_request_detail'
         ),
    path('technician/service-requests/<int:request_id>/update-status/',
         user_views.update_service_request_status,
         name='update_service_request_status'
         ),
    path('manager/dashboard/', user_views.manager_dashboard,
          name='manager_dashboard'
          ),
    path('manager/assign-request/<int:request_id>/', user_views.assign_service_request,
         name='assign_service_request'
         ),
    path(
        'manager/service-requests/<int:request_id>/',
        user_views.manager_service_request_detail,
        name='manager_service_request_detail'
        ),
    path("manager/technicians/", user_views.manager_technicians, 
         name="manager_technicians"
         ),
    path("manager/technicians/<int:technician_id>/", 
         user_views.manager_technician_detail, 
         name="manager_technician_detail"
         ),
    path('logout/', user_views.user_logout, name='logout'),
]

