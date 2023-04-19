from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import  status
from .validators import validate_file_extension
class SignUpSerializer(serializers.ModelSerializer) :
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True,allow_blank= True)
    resume = serializers.CharField(source='userprofile.resume' ,required = False,read_only= True)
    class Meta :
        model = User

        fields = ('first_name','last_name','username', 'email', 'password','password2','resume')
        extra_kwargs ={
            'first_name' :{'required' : True , 'allow_blank' : False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': { 'allow_blank': True,'min_length' : 6,'write_only': True},

        }


    def create(self,validate_data):

        password = self.validated_data['password']
        password2 = validate_data.pop('password2')

        if password != password2:
            raise serializers.ValidationError({"error": "Password  and Password 2 should be same"})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"error": "The email already exists"})



        account = User(**validate_data)
        account.set_password(password)
        account.save()

        return account



    def update(self,instance,validated_data):
            instance.username = validated_data.get('username',instance.username)
            instance.first_name = validated_data.get('first_name',instance.first_name)
            instance.last_name = validated_data.get('last_name',instance.last_name)
            instance.email = validated_data.get('last_name', instance.last_name)
            instance.username = validated_data.get('username', instance.username)
            if validated_data.get('password') != '':
                password = self.validated_data['password']
                password2 = self.validated_data['password2']

                if password != password2:
                    raise serializers.ValidationError({"error": "Password  and Password 2 should be same"})
                instance.set_password(validated_data.get('password'))
            instance.save()
            return instance

class UserInfoSerializer(serializers.ModelSerializer):
    resume = serializers.CharField(source='userprofile.resume')

    class Meta:
        model = User
        fields = ('first_name', 'last_name',  'email','username','resume')


