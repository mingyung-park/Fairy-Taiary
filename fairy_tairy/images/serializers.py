from rest_framework import serializers
import fairy_tairy.settings as settings
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

        

class ImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'