from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'address', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Company.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CompanyLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
