from django.contrib import admin
from django import forms
import re

# Register your models here.

from .models import Supersection, Section, Theme, Literature, Requirement, Theory, Problem, TaskSet
from .problems import problems_list_zip, unzip_problems

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


class TaskSetModelForm(forms.ModelForm):
            
    tasks = forms.CharField(widget=forms.TextInput(attrs={'size': '100'}) )

    def save(self, commit=True):
        tasks = self.cleaned_data.get('tasks', None)
        taskSet = super(TaskSetModelForm, self).save(commit=False)

        if taskSet.literature.literature_type == 'problems':
            new_tasks = unzip_problems(tasks)
            old_tasks = Problem.objects.filter(task_set=taskSet)
            for task in new_tasks:
                obj, created = Problem.objects.get_or_create(number=task, task_set=taskSet)
            for task in old_tasks:
                if task.number not in new_tasks:
                    task.delete()

        if taskSet.literature.literature_type == 'theory':
            new_tasks = tasks.split(',')
            old_tasks = Theory.objects.filter(task_set=taskSet)
            for task in new_tasks:
                pages = task.split('-')
                obj, created = Theory.objects.get_or_create(start_page=pages[0], end_page=pages[1], task_set=taskSet)
            for task in old_tasks:
                if task.__str__() not in new_tasks:
                    task.delete()

        taskSet.save()
        return taskSet
    
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            obj = kwargs['instance']
            tasks = []
            if obj.literature.literature_type == 'theory':
                for task in Theory.objects.filter(task_set=obj):
                    tasks += [f'{task.start_page}-{task.end_page}']
            elif obj.literature.literature_type == 'problems':
                for task in Problem.objects.filter(task_set=obj):
                    tasks += [task.number]
                tasks = problems_list_zip(tasks)
            kwargs.update({'initial': { 'tasks' : ', '.join(tasks) } })
        super(TaskSetModelForm, self).__init__(*args, **kwargs)
    

    class Meta:
        model = TaskSet
        fields = '__all__'

class TaskSetInline(admin.TabularInline):
    model = TaskSet
    form = TaskSetModelForm
    

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
    search_fields = ['number', 'task_set__theme__title', 'task_set__theme__full_title' , 'task_set__literature__title']

admin.site.register(Problem, ProblemAdmin)

# It is better to take page range instead of start_page
class TheoryAdmin(admin.ModelAdmin):
    list_display = ('start_page', 'task_set' )
    list_filter = ['task_set__difficulty']
    search_fields = ['start_page', 'end_page', 'task_set__theme__title', 'task_set__theme__full_title' , 'task_set__literature__title']


admin.site.register(Theory, TheoryAdmin)

class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'eng_title')
    list_filter = ['literature_type']
    search_fields = ['title']

admin.site.register(Literature, LiteratureAdmin)


class TaskSetAdmin(admin.ModelAdmin):
    list_display = ('theme', 'literature', 'difficulty')
    list_filter = ['difficulty']
    search_fields = ['theme__title','theme__full_title' ,'literature__title']

    inlines = [ProblemInline, TheoryInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        task_type = obj.literature.literature_type
        inlines = super(TaskSetAdmin, self).get_inline_instances(request, obj)
        for inline in inlines:
            if isinstance(inline, ProblemInline) and task_type == 'problems':
                return [inline]
            if isinstance(inline, TheoryInline) and task_type == 'theory':
                print(True)
                return [inline]
        return []
    
admin.site.register(TaskSet, TaskSetAdmin)

admin.site.register(Requirement)

