from rest_framework import serializers
#l'importe l'objet Q pour faciliter apartir de plusieurs champs
from django.db.models import Q
from . models import Profile
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import du jwt pour la gestion de token
from rest_framework_simplejwt.serializers import (
    TokenVerifySerializer # token de verification
)

User = get_user_model()

# User
# custom for the token verify
class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        data = super(CustomTokenVerifySerializer, self).validate(attrs)
        data.update({'detail': 'Token Successfuly Verify'})
        return data

class UserListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    names=serializers.CharField(max_length=255)    
    is_active=serializers.BooleanField()
    is_admin=serializers.BooleanField()
    staff=serializers.BooleanField()
    phone_number=serializers.CharField(max_length=25)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields=[ 'pk', 'email', 'names', 'is_active', 'is_admin', 'staff', 'phone_number', 'password2', 'date_add', 'date_update']

class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields=['email', 'names', 'password', 'password2', 'phone_number', 'staff']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        # recuperation des donnees
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        phone_number = attrs.get('phone_number')
        staff = attrs.get('staff')

        # validation du staff 
        if staff is None or "":
            raise serializers.ValidationError("Defined Staff of this User")
        # validation du password 
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't Match")
        # validation du mail
        email_exists=User.objects.filter(email=email).exists()
        if email_exists:
            raise serializers.ValidationError("User with Email Exists")
        # validation du numero de telephone
        phone_number_exists=User.objects.filter(phone_number=phone_number).exists()
        if phone_number_exists:
            raise serializers.ValidationError("User with Phone number Exists")
        return attrs        

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        # on recuper l'user courament connecter
        user = self.context.get('user')
        if password != password2:
          raise serializers.ValidationError("Password and Confirm Password doesn't Match")
        user.set_password(password)
        user.save()
        return attrs

class UserStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
    user_id = serializers.CharField(write_only=True, allow_null=False, allow_blank=False)

    class Meta:
        fields=[ 'pk', 'email', 'names', 'is_active', 'is_admin', 'staff', 'phone_number', 'password2', 'date_add', 'date_update']

    def validate(self, attrs):
        is_active = attrs.get('is_active')
        user_id = attrs.get('user_id')

        if is_active is None or "":
            raise serializers.ValidationError("The Status is None or Empty")
        if user_id is None or "":
            raise serializers.ValidationError("User is None or Empty")
        else:
            user_exists = User.objects.filter(id=user_id).exists()
            if user_exists:
                # on recuper l'user courament connecter
                user = User.objects.get(id=user_id)
                user.is_active = is_active
                user.save()
            else:
                raise serializers.ValidationError("User is Not Register")
            return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            # print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset your Password '+ link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')

# Profile
class ProfileSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    kind=serializers.CharField(max_length=25)
    adress=serializers.CharField(max_length=255)
    picture=serializers.ImageField(read_only=True)
    picture64 = serializers.CharField(write_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model=Profile
        fields=['pk', 'user', 'kind', 'adress', 'picture', 'picture64', 'date_add', 'date_update']
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1
    
    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        kind = attrs.get('kind')
        
        # validation du kind 
        if kind is None or "":
            raise serializers.ValidationError("Kind is None or Empty")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}

    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        # on supprimer certains elements du dict
        validated_data.pop('picture64')
        return Profile.objects.create(**validated_data)