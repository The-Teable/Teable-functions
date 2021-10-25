from rest_framework import serializers
from .models import Teas


class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teas
        fields = '__all__'
