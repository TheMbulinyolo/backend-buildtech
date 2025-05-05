from rest_framework import serializers
from .models import Participant

from rest_framework import serializers
from .models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'unique': 'Cet email est déjà utilisé.'
                }
            },
            'phone': {
                'error_messages': {
                    'invalid': 'Numéro de téléphone invalide.'
                }
            }
        }