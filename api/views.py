from django.shortcuts import render ,redirect
from django.http import HttpResponse 
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from rest_framework import status
from rest_framework.response import Response

def generate_editor_link(database_name,collection_name,fields,document_id):
    editor_url = "https://ll04-finance-dowell.github.io/100058-dowelleditor/?"
    return f"{editor_url}d_name={database_name}&col_name={collection_name}&id={document_id}&fields={fields}"


@csrf_exempt
def editor(request):
    if request.method == "POST":
        database =  request.POST.get('database', None)
        collection =  request.POST.get('collection', None)
        fields = request.POST.get('fields', None)
        document_id = request.POST.get('document_id', None) 
        generate_link = generate_editor_link(database,collection,fields,document_id)
        return JsonResponse({
            "editor_link":generate_link
            }) 
    else:
        return JsonResponse({
            "status":"Bad Requests? , something is wrong while posting !"
        })
