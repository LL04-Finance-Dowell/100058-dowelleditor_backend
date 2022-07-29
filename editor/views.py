import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from editor.utils import targeted_population, save_data_into_collection


class GetAllDataByCollection(View):

    def get(self, request):
        return HttpResponse(
            json.dumps(targeted_population('Documentation', 'TemplateReports', ['template_name'], 'life_time'),
                       indent=2, sort_keys=True))


@method_decorator(csrf_exempt, name='dispatch')
class PostDataIntoCollection(View):

    def post(self, request):
        database = request.POST.get('database', None)
        collection = request.POST.get('collection', None)
        id_ = request.POST.get('id', None)
        if database and collection and id_:
            return HttpResponse(json.dumps(save_data_into_collection(), indent=2, sort_keys=True))
        return JsonResponse({"info": "all parameters are required, database, collection, id"})
