# serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='get_school_name', read_only=True)
    section_name = serializers.CharField(source='get_section_name', read_only=True)
    school_id = serializers.CharField(source = 'get_school_id', read_only=True)
    section_id = serializers.CharField(source = 'get_section_id', read_only=True)
    class Meta:
        model = Student
        fields = ['roll_no', 'grade', 'name', 'school_name', 'section_name', 'points', 'updated_at', 'school_id', 'section_id']
