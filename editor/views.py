import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pyhtml2pdf import converter
import os
from .pdf import PdfGenerator 

from django.conf import settings

from editor.utils import (
    targeted_population,
    dowellconnection,
    single_query_document_collection,
    single_query_template_collection,
    access_editor,
    TEMPLATE_CONNECTION_LIST,
    TEMPLATE_METADATA_LIST,
    DOCUMENT_METADATA_LIST,
)
import jwt
import requests
from git.repo import Repo


class DeploymentWebhook(APIView):
    def post(self, request):
        try:
            repo = Repo("/home/100058/100058-dowelleditor_backend")
            origin = repo.remotes.origin
            origin.pull()
            return Response("Updated PA successfully", status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Wrong event Type!", status.HTTP_400_BAD_REQUEST)


class HealthCheck(APIView):
    def get(self, request):
        return Response(
            "If you are seeing this the editor is !down", status.HTTP_200_OK
        )


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
        cluster = request.data.get("cluster")
        database = request.data.get("database")
        collection = request.data.get("collection")
        document = request.data.get("document")
        team_member_ID = request.data.get("team_member_ID")
        function_ID = request.data.get("function_ID")
        document_id = request.data.get("document_id", None)

        field = {"_id": document_id}

        update_field = {"status": "success"}

        DATABASE = [
            cluster,
            database,
            collection,
            document,
            team_member_ID,
            function_ID,
        ]

        response_object = json.loads(
            dowellconnection(*DATABASE, "find", field, update_field)
        )

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
            # editor_url = f"https://ll04-finance-dowell.github.io/100058-dowelleditor/?token={encoded_jwt}"
            editor_url = f"https://ll04-finance-dowell.github.io/100058-DowellEditor-V2/?token={encoded_jwt}"
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
            if action == "template":
                field = {"_id": metadata_id}
                update_field = {"template_name": update_field["template_name"]}
                json.loads(
                    dowellconnection(
                        *TEMPLATE_METADATA_LIST, "update", field, update_field
                    )
                )
            if action == "document":
                field = {"_id": metadata_id}
                update_field = {"document_name": update_field["document_name"]}
                json.loads(
                    dowellconnection(
                        *DOCUMENT_METADATA_LIST, "update", field, update_field
                    )
                )
            return Response(response, status=status.HTTP_200_OK)
        return Response({"info": "Sorry!"}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class GeneratePDFLink(APIView):
    def post(self, request):
        item_id = request.data.get("item_id")
        item_type = request.data.get("item_type")

        if not item_id and not item_type:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        
        if item_type == "document":
            item = single_query_document_collection({"_id": item_id})
            if item:
                item_name = item.get("document_name")
            else:
                return Response("document does not exist",status=status.HTTP_400_BAD_REQUEST)
            
        elif item_type == "template":
            item = single_query_template_collection({"_id": item_id})
            if item:
                item_name = item.get("template_name")
            else:
                return Response("template does not exist",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("invalid Item type", status=status.HTTP_400_BAD_REQUEST)
        

        link = access_editor(item_id, item_type)
        res = requests.get(url=link)

        if res.status_code == 200:
            try:
                pdf_file = PdfGenerator([link]).main()
                with open(f"{item_name}.pdf", "wb") as outfile:
                    outfile.write(pdf_file[0].getbuffer())

                pdf_storage_url = "https://dowellfileuploader.uxlivinglab.online/uploadfiles/upload-pdf-file/"
                pdf_file_path = f"{item_name}.pdf"
                files = {"pdf": open(pdf_file_path, "rb")}

                response = requests.post(pdf_storage_url, files=files)

                pdf_link = json.loads(response.content)
                os.remove(pdf_file_path)

                if response.status_code == 201:
                    return Response(
                        pdf_link["file_url"], status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        "Error encountered during PDF generation",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            except Exception as error:
                return Response(
                    f"PDF conversion failed: {error}",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                "Failed to access the document",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
