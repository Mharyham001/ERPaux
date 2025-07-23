from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_request, name='submit_request'),
    path('requests/', views.view_requests, name='view_requests'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('rfq/send/<int:material_id>/', views.send_rfq, name='send_rfq'),
    path('rfq/list/', views.rfq_list, name='rfq_list'),
]
