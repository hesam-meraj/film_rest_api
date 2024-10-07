from django.shortcuts import render
# from django.shortcuts import HttpResponse
# from django.http import JsonResponse 
from film_app.models import *
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import FilmSerializer 
import json
@api_view(['GET', 'POST'])
def api_home(requset):
    '''
    DRF API VIEW
    '''
    instance = Film.objects.all().order_by("?").first()
    data = {}
    if instance:
        # data = model_to_dict(data)
        data = FilmSerializer(instance).data
    return Response(data)



