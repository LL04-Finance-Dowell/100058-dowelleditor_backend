from django.urls import path

from api.views import editor , link_generator

urlpatterns =[
    path('editor/',editor, name= 'api_editor'),
    path('link_generator/',link_generator, name= 'link_generator'),
]