import json
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.utils.safestring import SafeString

from .models import Olympiad, OlympEvent, OlympFile
from django.db.models import Max
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, 'upho/index.html')

def olympiads(request, olymp_type='national', static_location=''):
    olympiad = Olympiad.objects.get(olymp_type=olymp_type)

    # Default static location for regional
    if (olymp_type == 'regional' and static_location == ''):
        static_location = 'KYIV'

    # List of locations
    location_list = []
    for location_type in OlympEvent.LOCATION_CHOICES:
        location_list += list(location_type[1])

    print(location_list)

    # All options for olympiad (each has at least one corresponding olympiad file)
    years = {tour : list(OlympEvent.objects.filter(olympiad=olympiad, olympfile__tour=tour, location__contains=static_location).order_by('-year').values_list('year', flat=True).distinct()) for tour in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location).values_list('tour', flat=True).distinct())}
    grades = {tour : list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location, tour=tour).order_by('-grade').values_list('grade', flat=True).distinct()) for tour in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location).values_list('tour', flat=True).distinct())}
    tours = [{ "tour" : tour[0], "readable" : tour[1] } for tour in OlympFile.TOUR_CHOICES if OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location, tour=tour[0]).exists() ]
    locations = { year : dict(location_list)[OlympEvent.objects.get(olympiad=olympiad, year=year, location__contains=static_location).location] for year in list(OlympEvent.objects.filter(olympiad=olympiad, location__contains=static_location).values_list('year', flat=True).distinct()) }
    olymp_options = {"years" : years, "grades" : grades, "tours" : tours, "locations" : locations}

    # Information about all files in structured way
    olymp_files ={ olymp_files :  {tour : {f"{grade}" : list(OlympEvent.objects.filter(olympiad=olympiad, location__contains=static_location, olympfile__tour=tour, olympfile__grade=grade, olympfile__solutions=False if olymp_files=='problems' else True).values_list('year', flat=True).distinct()) for grade in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location, tour=tour).values_list('grade', flat=True).distinct()) } for tour in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location).values_list('tour', flat=True).distinct()) } for olymp_files in ['problems', 'solutions'] }

    # Info about olympiad
    olymp_info = { "olymp_type" : olymp_type, "olymp_name" : Olympiad.objects.get(olymp_type=olymp_type).name , "static_location" : { "name" : static_location.lower(), "readable" : "" if static_location=="" else dict(location_list)[static_location.upper()] } }

    # List of regional locations (each has at least one corresponding olympiad file)
    regional_locations = [{ "name" : location, "readable" : dict(location_list)[location] } for location in list(OlympEvent.objects.filter(olympiad__olymp_type="regional").values_list('location', flat=True).distinct()) ]

    context = {"olymp_info" : olymp_info, "olymp_options" : SafeString(olymp_options) , "olymp_files" : SafeString(olymp_files), "regional_locations" : SafeString(regional_locations)}
    return render(request, f"upho/olympiad.html", context)

