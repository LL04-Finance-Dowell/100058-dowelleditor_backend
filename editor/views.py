import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from editor.utils import (
    targeted_population,
    filter_id,
    get_event_id,
    dowellconnection,
    DOCUMENT_CONNECTION_LIST,
    TEMPLATE_CONNECTION_LIST,
    TEMPLATE_METADATA_LIST,
    DOCUMENT_METADATA_LIST
)
import jwt
import requests


@method_decorator(csrf_exempt, name="dispatch")
class GetAllDataByCollection(APIView):
    def post(self, request):
        database = request.data.get("database", None)
        collection = request.data.get("collection", None)
        fields = request.data.get("fields", None)
        _id = request.data.get("id", None)
        if database and collection and fields:
            response = targeted_population(database, collection, [fields], "life_time")

            def reports(mongo_id):
                found_document = {}
                for i in response["normal"]["data"][0]:
                    if i["_id"] == mongo_id:
                        found_document = i
                        return found_document
                return found_document

            return Response(reports(_id), status=status.HTTP_200_OK)
        return Response(
            {"info": "all parameters are required, database, collection, fields"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# @method_decorator(csrf_exempt, name="dispatch")
# class GetAllDataFromCollection(APIView):
#     def post(self, request):
#         if request.method == "POST":
#             document_id = request.data.get("document_id", None)
#             action = request.data.get("action", None)
            
#             field = {
#                 "_id": document_id
#             }
          
#             update_field = {
#                 "status": "success"
#             }
          
#             if action == "template":
              
#                 response_obj = dowellconnection(*TEMPLATE_CONNECTION_LIST, "find", field, update_field)
#                 data = json.loads(response_obj)
            
#                 try:
#                     if len(data["data"]):
#                         return Response(data["data"], status=status.HTTP_200_OK)
#                 except:
#                     return Response([], status=status.HTTP_204_NO_CONTENT)
#             elif action == "document":
#                 response_obj = dowellconnection(
#                     *DOCUMENT_CONNECTION_LIST, "find", field, update_field
#                 )
#                 data = json.loads(response_obj)
#                 try:
#                     if len(data["data"]):
#                         return Response(data["data"], status=status.HTTP_200_OK)
#                 except:
#                     return Response([], status=status.HTTP_204_NO_CONTENT)
#         return Response({"info": "Sorry!"}, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(csrf_exempt, name="dispatch")
class GetAllDataFromCollection(APIView):
    def post(self, request):
    
        cluster = request.data.get("cluster")
        database = request.data.get("database")
        collection = request.data.get("collection")
        document = request.data.get("document")
        team_member_ID = request.data.get("team_member_ID")
        function_ID = request.data.get("function_ID")
        document_id = request.data.get("document_id", None)
        
        field = {
            "_id": document_id
        }
        
        update_field = {
            "status": "success"
        }

        DATABASE = [
            cluster, database, collection, document,team_member_ID, function_ID
        ]
        
        response_object = json.loads(dowellconnection(*DATABASE,"find",field,update_field))
            
        try:
            if len(response_object["data"]):
                return Response(response_object["data"], status=status.HTTP_200_OK)
        except:
            return Response([], status=status.HTTP_204_NO_CONTENT)
    


@method_decorator(csrf_exempt, name="dispatch")
class GenerateEditorLink(APIView):
    def post(self, request):
        if request.method == "POST":
            encoded_jwt = jwt.encode(
                json.loads(request.body), "secret", algorithm="HS256"
            )
            editor_url = f"https://ll04-finance-dowell.github.io/100058-dowelleditor/?token={encoded_jwt}"
            return Response(editor_url, status=status.HTTP_200_OK)
        return Response({"info": "toodles!!"}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class SaveIntoCollection(APIView):
    def post(self, request):
        if request.method == "POST":
            cluster = json.loads(request.body)["cluster"]
            database = json.loads(request.body)["database"]
            collection = json.loads(request.body)["collection"]
            document = json.loads(request.body)["document"]
            team_member_ID = json.loads(request.body)["team_member_ID"]
            function_ID = json.loads(request.body)["function_ID"]
            command = json.loads(request.body)["command"]
            field = json.loads(request.body)["field"]
            update_field = json.loads(request.body)["update_field"]
            action = json.loads(request.body)["action"]
            metadata_id = json.loads(request.body)["metadata_id"]
            response = dowellconnection(cluster,database,collection,document,team_member_ID,function_ID,command,field,update_field)

            print("------------",update_field["template_name"])
            print("------------",action)
            print("------------",metadata_id)
            print("------------")
            if action == "template":
                field = {
                    "_id": metadata_id
                }
                update_field = {
                    "template_name": update_field["template_name"]
                }
                update_name = json.loads(dowellconnection(*TEMPLATE_METADATA_LIST,"update",field, update_field))
                print("----------------",update_name)
            if action == "document":
                field = {
                    "_id": metadata_id
                }
                update_field = {
                    "document_name": update_field["document_name"]
                }
                update_name = json.loads(dowellconnection(*DOCUMENT_METADATA_LIST,"update",field, update_field))
                print("----------------",update_name)

            return Response(response, status=status.HTTP_200_OK)
        return Response({"info": "Sorry!"}, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name="dispatch")
class test(APIView):
    def post(self, request):
        field = {
            "_id":"649d89a5429329158cccaaaa"
        }
        update_field = {
            "status": "success"
        }

        response = dowellconnection(*TEMPLATE_CONNECTION_LIST, "find", field ,update_field)

        return Response(response, status=status.HTTP_200_OK)