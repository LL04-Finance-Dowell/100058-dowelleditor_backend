import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from editor.utils import targeted_population, save_data_into_collection, filter_id


@method_decorator(csrf_exempt, name='dispatch')
class GetAllDataByCollection(APIView):

    def post(self, request):
        database = request.data.get('database', None)
        collection = request.data.get('collection', None)
        fields = request.data.get('fields', None)
        if database and collection and fields:
            return HttpResponse(
                json.dumps(targeted_population(database, collection, [fields], 'life_time'),
                           indent=2, sort_keys=True))
        return JsonResponse({"info": "all parameters are required, database, collection, fields"})


@method_decorator(csrf_exempt, name='dispatch')
class PostDataIntoCollection(APIView):

    def post(self, request):
        database = request.data.get('database', None)
        collection = request.data.get('collection', None)
        fields = request.data.get('fields', None)
        if database and collection and fields:
            res = save_data_into_collection(database, collection, fields)
            population_res = targeted_population(database, collection, ['_id'], 'life_time')
            if filter_res := filter_id('_id', res['inserted_id'], population_res['normal']['data'][0]):
                return Response(
                    json.dumps(filter_res, indent=2, sort_keys=True))
        return JsonResponse({"info": "all parameters are required, database, collection, fields"})
