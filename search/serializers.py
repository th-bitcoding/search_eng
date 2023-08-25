from rest_framework import serializers
from .models import *

        
class SubObjectJSONSerializer(serializers.ModelSerializer):
    sub_objects = serializers.JSONField()
    
    
    class Meta:
        model = SubObjectJSON
        fields = '__all__'