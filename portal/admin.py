from django.contrib import admin
from portal.models import Patient, Doctor, Appointment

""" class TasksAdmin(admin.ModelAdmin):
    fields = ('task_board','title','description', 'author', 'due_date') 
    list_display = ('task_board','title','description', 'author', 'due_date', 'priority')
    search_fields = ('title',) """



admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
