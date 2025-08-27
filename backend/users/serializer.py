from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'rol']
        
        def create(self, validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user)
            return user
        
class UserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    phone_code = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'user',
            'number_id',
            'age',
            'phone_code',
            'phone_number',
            'phone',
            'country',
            'city',
            'address',
            'photo',
        ]
        read_only_fields = ['phone']
        
    def create(self, validated_data):
        phone_code = validated_data.pop('phone_code')
        phone_number = validated_data.pop('phone_number')
        validated_data['phone'] = f"+{phone_code}{phone_number}"
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        phone_code = validated_data.pop('phone_code', None)
        phone_number = validated_data.pop('phone_number', None)
        if phone_code and phone_number:
            validated_data['phone'] = f"+{phone_code}{phone_number}"
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.phone:
            parts = instance.phone.strip().split()
            if len(parts) >= 2:
                rep["phone_code"] = parts[0]
                rep["phone_number"] = " ".join(parts[1:])
        return rep