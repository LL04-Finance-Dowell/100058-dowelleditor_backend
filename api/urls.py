from django.urls import path

from api.views import editor , get_link

urlpatterns =[
    path('editor/',editor, name= 'api_editor'),
    path('get-link/', get_link,name="get-link"),
]