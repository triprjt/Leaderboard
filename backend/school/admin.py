from django.contrib import admin

# Register your models here.
from .models import Student, Section, School

admin.site.register(Student)
admin.site.register(Section)
admin.site.register(School)

