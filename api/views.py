from django.shortcuts import render ,redirect
from django.http import HttpResponse 
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from rest_framework import status
from rest_framework.response import Response

from api.utils import dowellconnection
from api.utils import get_event_id

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
@csrf_exempt
def get_link(request):
    if request.method == "GET":
        field = {
            "eventId":get_event_id(),
            "created_by":"Manish",
            "company_id":"555553",
            "template_name":"",
            "content": "",
        }
        update_field= {
            "order_nos": 21
        }
        response= dowellconnection("Documents","Documentation","editor","editor","100084006","ABCDE","insert",field,update_field)
        print("<------response----->",response)
        url="https://100058.pythonanywhere.com/api/generate-editor-link/"
        payload = json.dumps({
            "product_name": "workflowai",
            "details":{
                "_id":response,
                "action":"template",
                "field":"template_name",
                "cluster": "Documents",
                "database": "Documentation",
                "collection": "editor",
                "document": "editor",
                "team_member_ID": "100084006",
                "function_ID": "ABCDE",
                "command": "update",
                "update_field": {
                "template_name":"",
                "content":""
                }
            }
        })
        responses = requests.request("POST", url,data=payload)
        return JsonResponse({"link":responses.text})
