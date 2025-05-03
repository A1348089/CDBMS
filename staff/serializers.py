from rest_framework import serializers
from .models import Staff

from datetime import date

class StaffSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.departmentName', read_only=True)  # Fetch department name
    experience = serializers.SerializerMethodField()  # Compute experience dynamically

    def get_experience(self, obj):
        if obj.doj_in_govt_service:
            return date.today().year - obj.doj_in_govt_service.year
        return "N/A"
    
    class Meta:
        model = Staff
        fields = '__all__'