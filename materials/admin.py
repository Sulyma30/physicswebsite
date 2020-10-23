from django.contrib import admin

# Register your models here.

from .models import Supersection, Section, Theme, Literature, Requirement, Theory, Problem, TaskSet

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

class TaskSetInline(admin.TabularInline):
    model = TaskSet
    extra = 1

# Should be improved to show separately binded problems and theories. Under or above is option to add list of numbers or pages that correspond to the creation of the same number of model instances
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'section')
    list_filter = ['section']
    search_fields = ['title', 'full_title']
    ordering = ['order']
    inlines = [TaskSetInline]

admin.site.register(Theme, ThemeAdmin)

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('number', 'task_set')
    list_filter = ['task_set__difficulty']
    search_fields = ['number', 'theme__title', 'theme__full_title' , 'literature__title']

admin.site.register(Problem, ProblemAdmin)

# It is better to take page range instead of start_page
class TheoryAdmin(admin.ModelAdmin):
    list_display = ('start_page', 'task_set' )
    list_filter = ['task_set__difficulty']
    search_fields = ['start_page', 'end_page', 'theme__title', 'theme__full_title' , 'literature__title']


admin.site.register(Theory, TheoryAdmin)

class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'eng_title')
    list_filter = ['literature_type']
    search_fields = ['title']

admin.site.register(Literature, LiteratureAdmin)

class TaskSetAdmin(admin.ModelAdmin):
    list_display = ('theme', 'literature')
    list_filter = ['difficulty']
    search_fields = ['theme', 'literature']
    inlines = [ProblemInline]

admin.site.register(TaskSet, TaskSetAdmin)