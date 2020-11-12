from django.contrib import admin
from django import forms
import re

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


class TaskSetModelForm(forms.ModelForm):
            
    tasks = forms.CharField(widget=forms.TextInput(attrs={'size': '100'}) )

    def save(self, commit=True):
        tasks = self.cleaned_data.get('tasks', None)
        # With info below I can get TaskSet, transform tasks and do the following:
        # get all tasks before they were changed (the same taskset) and compare with the new set; then delete or add or change (difficulty) every task that was deleted or added. It sufficient to use get_or_create when create a new one (for example, when this task already exists with another difficulty)
        print(self.cleaned_data.get('difficulty', None))
        print(self.cleaned_data.get('literature', None))
        print(self.cleaned_data.get('theme', None))
        print(tasks)
        return super(TaskSetModelForm, self).save(commit=commit)
    
    def problems_list_zip(self, start_list):
        #this function converts sorted list of problems into zip one using "-"
        #example: from ["1.1","1.2","1.3","1.5","1.6","1.7","2.1","2.2"]
        #         to   ["1.1-3,5-7","2.1,2"]

        #this function is divide in two parts. First zip all ranges and second join problems with same "id"
        #example for the first part:
        #from ["1.1","1.2","1.3","1.5","1.6","1.7","2.1","2.2"]
        #to   ["1.1-3","1.5-7","2.1,2"]

        #example for the second part:
        #from ["1.1-3","1.5-7","2.1,2"]
        #to   ["1.1-3,5-7","2.1,2"]
        middle_list = []
        if not (re.match("^((\d+\.)*)(\d+)$",start_list[0])):
            raise TypeError("Wrong problems format")#maybe here should be specification exactly what problem have wrong format
            
        reg_exp = re.search("^((\d+\.)*)(\d+)$",start_list[0])
        range_id, first_num = reg_exp.group(1), int(reg_exp.group(3)) #if element="1.2.3.4", range_id ="1.2.3." and first_num=4
        prev_num = first_num
        count = 1 #quantity of problems in range
        
        for element in start_list[1:]:
            if not (re.match("^((\d+\.)*)(\d+)$",element)):
                raise TypeError("Wrong problems format")#maybe here should be specification exactly what problem have wrong format
            
            reg_exp = re.search("^((\d+\.)*)(\d+)$",element)
            element_id, element_num = reg_exp.group(1), int(reg_exp.group(3))
            if (element_id != range_id) or (prev_num + 1 != element_num): #range ended
                if count > 2:
                    middle_list.append(f"{range_id}{first_num}-{prev_num}")
                elif count == 2: middle_list.append(f"{range_id}{first_num},{prev_num}")
                else:middle_list.append(f"{range_id}{first_num}")
                    
                range_id, first_num = element_id, element_num
                prev_num = first_num
                count = 1 
            else:
                prev_num += 1
                count += 1
        if count > 2:
            middle_list.append(f"{range_id}{first_num}-{prev_num}")
        elif count == 2: middle_list.append(f"{range_id}{first_num},{prev_num}")
        else:middle_list.append(f"{range_id}{first_num}")


        #here second part begins
        final_list = []
        reg_exp = re.search("^((\d+\.)*)([\d,-]+)$",middle_list[0])
        section_id, num_string = reg_exp.group(1), reg_exp.group(3) #if element="1.2.3.4-10", section_id ="1.2.3.", num_string = "4-10"
        
        for element in middle_list[1:]:
            reg_exp = re.search("^((\d+\.)*)([\d,-]+)$",element)
            element_id, el_string = reg_exp.group(1), reg_exp.group(3)
            if (element_id != section_id): #range ended
                final_list.append(section_id + num_string)
                    
                section_id, num_string = element_id, el_string
            else:
                num_string = num_string + "," + el_string
        final_list.append(section_id + num_string)


        
        return final_list
    
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
                tasks = self.problems_list_zip(tasks)
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
    form = TaskSetModelForm

    inlines = [ProblemInline]
    
admin.site.register(TaskSet, TaskSetAdmin)

admin.site.register(Requirement)

