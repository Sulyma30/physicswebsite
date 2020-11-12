import json
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import JsonResponse

from .models import Olympiad, OlympEvent, OlympFile, Location
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import OlympiadEventSerializer

# Create your views here.
def index(request):
    return render(request, 'upho/index.html')

def olympiad_page(request, olymp_type='national', static_location=''):
    olympiad = get_object_or_404(Olympiad, olymp_type=olymp_type)
    if olymp_type == 'regional' and static_location == '':
        location = 'KYIV'
    else:
        location = static_location
    regions = Location.objects.filter(olympevent__olympiad__olymp_type='regional').distinct()
    return render(request, 'upho/olympiad.html', { "olympiad" : olympiad, "static_location" : location, "regions" : regions })

@api_view(['GET'])
def olympiad(request, olymp_type='national', static_location=''):
    olympiad = get_list_or_404(Olympiad, olymp_type=olymp_type)
    events = OlympEvent.objects.filter(olympiad__olymp_type=olymp_type, location__name__contains=static_location).order_by('-year')
    serializer = OlympiadEventSerializer(events, many=True)
    return Response(serializer.data)

def ipho(request):
    return render(request, "upho/ipho.html")
