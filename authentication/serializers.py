from django.contrib.auth import update_session_auth_hash
 
from rest_framework import serializers
 
from .models import Account
 
 
class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
 
    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'tagline', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at')
 
        def create(self, validation_data):
            return Account.objects.create(**validation_data)
 
        def update(self, instance, validation_data):
            instance.username = validation_data.get('username', instance.username)
            instance.tagline = validation_data.get('tagline', instance.tagline)
 
            instance.save()
 
            password = validation_data.get('password', None)
            confirm_password = validation_data.get('confirm_password', None)
 
            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()
 
            update_session_auth_hash(self.context.get('request'), instance)
 
            return instance