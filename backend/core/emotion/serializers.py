from rest_framework import serializers
from .models import EEGSignal
from datetime import datetime

class EEGFeaturesSerializer(serializers.Serializer):
    Mean = serializers.FloatField()
    Max = serializers.FloatField()
    Standard_Deviation = serializers.FloatField()
    RMS = serializers.FloatField()
    Peak_to_Peak = serializers.FloatField()
    Abs_Diff_Signal = serializers.FloatField()
    Alpha_Power = serializers.FloatField()


class EEGSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EEGSignal
        fields = ['Mean', 'Max', 'Standard_Deviation', 'RMS', 'Peak_to_Peak', 'Abs_Diff_Signal', 'Alpha_Power', 'timestamp']
    
    def create(self, validated_data):
        # Add timestamp to the validated data
        validated_data['timestamp'] = datetime.now()
        return EEGSignal.objects.create(**validated_data)
