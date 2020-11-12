from django.contrib import admin
from django.forms import inlineformset_factory, ModelForm
from django.forms import BaseInlineFormSet

# Register your models here.
from .models import Olympiad, OlympEvent, OlympFile, Location

class OlympFileInlineAdminForm(ModelForm):
    class Meta:
        model = OlympFile
        fields = ['grade', 'tour', 'problems', 'solutions']

class OlympFileFormSet(BaseInlineFormSet):
    # Prepopulate inlines with grade, tour and solutions if it is not in already uploaded files (exist_files)
    def __init__(self, *args, **kwargs):
        event = kwargs['instance']
        exist_files = []
        # Check whether we create a new event or modify one
        if (event.pk != None ):
            exist_files = OlympFile.objects.filter(event__olympiad=event.olympiad, event__location=event.location, event__year=event.year).values_list('grade', 'tour')
        kwargs.update({'initial': [{ 'grade' : grade, 'tour' : tour } for grade, tour in [(0, 'theory'), (0, 'exp'), (11, 'theory'), (11, 'exp'), (10, 'theory'), (10, 'exp') ,(9, 'theory'), (9, 'exp'), (8, 'theory'), (8, 'exp')] if (grade, tour) not in exist_files ]})
        super(OlympFileFormSet, self).__init__(*args, **kwargs)
  

class OlympFileInline(admin.TabularInline):
    model = OlympFile
    form = OlympFileInlineAdminForm
    formset = OlympFileFormSet
    ordering = ['-grade']
    extra = 10


class OlympEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'olympiad', 'location')
    list_filter = ['olympiad']
    search_fields = ['year', 'location']
    ordering = ['-year']
    inlines = [OlympFileInline,]

admin.site.register(OlympEvent, OlympEventAdmin)
admin.site.register(Location)