from django.contrib import admin
from django.forms import inlineformset_factory, ModelForm
from django.forms import BaseInlineFormSet

# Register your models here.
from .models import Supersection, Section, Theme, Literature, Requirement, Theory, Problem,Olympiad, OlympEvent, OlympFile

class SectionInline(admin.TabularInline):
    model = Section
    ordering = ['order']

class SupersectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ['order']
    inlines = [SectionInline]

admin.site.register(Supersection, SupersectionAdmin)

class ThemeInline(admin.TabularInline):
    model = Theme
    ordering = ['order']

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'supersection')
    list_filter = ['supersection']
    search_fields = ['title']
    ordering = ['order']
    inlines = [ThemeInline]

admin.site.register(Section, SectionAdmin)

class ProblemInline(admin.TabularInline):
    model = Problem
    extra = 1

class TheoryInline(admin.TabularInline):
    model = Theory
    extra = 1

# Should be improved to show separately binded problems and theories. Under or above is option to add list of numbers or pages that correspond to the creation of the same number of model instances
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'section')
    list_filter = ['section']
    search_fields = ['title', 'full_title']
    ordering = ['order']
    inlines = [ProblemInline, TheoryInline]

admin.site.register(Theme, ThemeAdmin)

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('number', 'literature', 'theme', 'difficulty' )
    list_filter = ['difficulty']
    search_fields = ['number', 'theme__title', 'theme__full_title' , 'literature__title']

admin.site.register(Problem, ProblemAdmin)

# It is better to take page range instead of start_page
class TheoryAdmin(admin.ModelAdmin):
    list_display = ('start_page', 'literature', 'theme', 'difficulty' )
    list_filter = ['difficulty']
    search_fields = ['start_page', 'end_page', 'theme__title', 'theme__full_title' , 'literature__title']


admin.site.register(Theory, TheoryAdmin)

class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'eng_title')
    list_filter = ['literature_type']
    search_fields = ['title']

admin.site.register(Literature, LiteratureAdmin)

class OlympFileInlineAdminForm(ModelForm):
    class Meta:
        model = OlympFile
        fields = ['grade', 'tour', 'solutions', 'pdf']

class OlympFileFormSet(BaseInlineFormSet):
    # Prepopulate inlines with grade, tour and solutions if it is not in already uploaded files (exist_files)
    def __init__(self, *args, **kwargs):
        event = kwargs['instance']
        exist_files = []
        # Check whether we create a new event or modify one
        if (event.pk != None ):
            exist_files = OlympFile.objects.filter(event__olympiad=event.olympiad, event__location=event.location, event__year=event.year).values_list('grade', 'tour', 'solutions')
        kwargs.update({'initial': [{ 'grade' : grade, 'tour' : tour, 'solutions' : solutions } for grade, tour, solutions in [(0, 'theory', False),(0, 'theory', True), (0, 'exp', False),(0, 'exp', True), (11, 'theory', False),(11, 'theory', True), (11, 'exp', False),(11, 'exp', True),(10, 'theory', False),(10, 'theory', True), (10, 'exp', False),(10, 'exp', True),(9, 'theory', False),(9, 'theory', True), (9, 'exp', False),(9, 'exp', True),(8, 'theory', False),(8, 'theory', True), (8, 'exp', False),(8, 'exp', True)] if (grade, tour, solutions) not in exist_files ]})
        super(OlympFileFormSet, self).__init__(*args, **kwargs)
  

class OlympFileInline(admin.TabularInline):
    model = OlympFile
    form = OlympFileInlineAdminForm
    formset = OlympFileFormSet
    ordering = ['-grade']
    extra = 20


class OlympEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'olympiad', 'location')
    list_filter = ['olympiad']
    search_fields = ['year', 'location']
    ordering = ['-year']
    inlines = [OlympFileInline,]

admin.site.register(OlympEvent, OlympEventAdmin)

# Requirements !!!