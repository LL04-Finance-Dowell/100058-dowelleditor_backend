import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from editor.utils import targeted_population, filter_id , get_event_id, dowellconnection


@method_decorator(csrf_exempt, name='dispatch')
class GetAllDataByCollection(APIView):

    def post(self, request):
        database = request.data.get('database', None)
        collection = request.data.get('collection', None)
        fields = request.data.get('fields', None)
        _id= request.data.get('id', None)
        if database and collection and fields:
            response=targeted_population(database, collection, [fields], 'life_time')
            def reports(mongo_id):
                found_document = {}
                for i in response['normal']['data'][0]:
                    if i['_id'] == mongo_id:
                        found_document = i
                        return found_document
                return found_document
            return Response(reports(_id),status=status.HTTP_200_OK)
        return Response({"info": "all parameters are required, database, collection, fields"},
                        status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class PostDataIntoCollection(APIView):

    def post(self, request):
        if request.method == "POST":
            raw_data = request.data.get('raw_data', None)
            edited_data = request.data.get('edited_data', None)
            field ={
                "eventId":get_event_id(),
                "raw_data": raw_data,
                "edited_data":edited_data
            }
            inserted_id= dowellconnection("Documents","Documentation","editor","editor","100084006","ABCDE","insert",field)
            return Response(inserted_id,status=status.HTTP_200_OK)
        return Response({"info": "Sorry!"},status=status.HTTP_400_BAD_REQUEST)
         

