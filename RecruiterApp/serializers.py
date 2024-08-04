from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        company = Company(
            name=validated_data['name'],
            email=validated_data['email'],
            address=validated_data['address'],
        )
        company.set_password(validated_data['password'])
        company.save()
        return company