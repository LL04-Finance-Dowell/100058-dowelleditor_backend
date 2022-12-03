from django.urls import path
from .views import *

urlpatterns = [
    path('get-data-by-collection/', GetAllDataByCollection.as_view()),
    path('post-data-into-collection/', PostDataIntoCollection.as_view()),
    path('generate-editor-link/', GenerateEditorLink.as_view()),
    path('save-data-into-collection/', SaveIntoCollection.as_view()),
    
]
