from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.college_name')
    program_short_name = serializers.CharField(source='program.program_short_name', read_only=True)
    subject_combination_short_name = serializers.CharField(source='subject_combination.combination_short_form', read_only=True)
    medium = serializers.CharField(source='medium.medium',read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__' 