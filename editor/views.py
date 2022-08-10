from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from editor.utils import targeted_population, filter_id


@method_decorator(csrf_exempt, name='dispatch')
class GetAllDataByCollection(APIView):

    def post(self, request):
        database = request.data.get('database', None)
        collection = request.data.get('collection', None)
        fields = request.data.get('fields', None)
        if database and collection and fields:
            return Response(targeted_population(database, collection, [fields], 'life_time'), status=status.HTTP_200_OK)
        return Response({"info": "all parameters are required, database, collection, fields"},
                        status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PostDataIntoCollection(APIView):

    def post(self, request):
        database = request.data.get('database', None)
        collection = request.data.get('collection', None)
        fields = request.data.get('fields', None)
        if database and collection and fields:
            field_name = fields['field_name']
            population_res = targeted_population(database, collection, [field_name], 'life_time')
            if filter_res := filter_id('_id', fields['inserted_id']['inserted_id'],
                                       population_res['normal']['data'][0]):
                return Response(filter_res, status=status.HTTP_200_OK)
        return Response({"info": "all parameters are required, database, collection, fields"},
                        status=status.HTTP_400_BAD_REQUEST)
