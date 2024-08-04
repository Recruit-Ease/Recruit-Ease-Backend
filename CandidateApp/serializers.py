from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        candidate = Candidate(
            name=validated_data['name'],
            email=validated_data['email'],
        )
        candidate.set_password(validated_data['password'])
        candidate.save()
        return candidate