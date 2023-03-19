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


@method_decorator(csrf_exempt, name="dispatch")
class GetAllDataFromCollection(APIView):
    def post(self, request):
        if request.method == "POST":
            document_id = request.data.get("document_id", None)
            action = request.data.get("action", None)
            fields = {"_id": document_id}
            if action == "template":
                response_obj = dowellconnection(
                    *TEMPLATE_CONNECTION_LIST, "find", fields, "nill"
                )
                try:
                    if len(response_obj["data"]):
                        return Response(response_obj["data"], status=status.HTTP_200_OK)
                except:
                    return Response([], status=status.HTTP_204_NO_CONTENT)
            elif action == "document":
                response_obj = dowellconnection(
                    *DOCUMENT_CONNECTION_LIST, "find", fields, "nill"
                )
                try:
                    if len(response_obj["data"]):
                        return Response(response_obj["data"], status=status.HTTP_200_OK)
                except:
                    return Response([], status=status.HTTP_204_NO_CONTENT)
        return Response({"info": "Sorry!"}, status=status.HTTP_400_BAD_REQUEST)


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
            response = dowellconnection(
                cluster,
                database,
                collection,
                document,
                team_member_ID,
                function_ID,
                command,
                field,
                update_field,
            )
            return Response(response, status=status.HTTP_200_OK)
        return Response({"info": "Sorry!"}, status=status.HTTP_400_BAD_REQUEST)
