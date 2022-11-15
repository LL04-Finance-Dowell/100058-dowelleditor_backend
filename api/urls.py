from django.urls import path

from api.views import editor

urlpatterns =[
    path('editor/',editor, name= 'api_editor'),
]