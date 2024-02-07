from .views import *
from django.urls import path

app_name = 'Chatbot'

urlpatterns=[
    path('',chatview,name='chatbot'),
]
