from rest_framework import serializers
#l'importe l'objet Q pour faciliter apartir de plusieurs champs
from django.db.models import Q
from identification.models import Parcel
from . models import (
    Agent,
    Profile, 
    Function,
    Assignment,
    Rate,
    Station,
    Usage,
    Buy_Mode
)
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
# Agent
class AgentSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(read_only=True)
    email=serializers.EmailField(max_length=255, allow_null=False, allow_blank=False)
    names=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    is_active=serializers.BooleanField(default=True)
    phone_number=serializers.CharField(max_length=25, allow_null=False, allow_blank=False)

    class Meta:
        model=Agent
        fields=['pk', 'user', 'email', 'names', 'is_active', 'phone_number', 'date_add', 'date_update']
    
    def __init__(self, *args, **kwargs):
        super(AgentSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1  
    
    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        email = attrs.get('email')
        names = attrs.get('names')
        phone_number = attrs.get('phone_number')

        # validation 
        if email is None or "":
            raise serializers.ValidationError("Email is None or Empty")
        if names is None or "":
            raise serializers.ValidationError("Names is None or Empty")
        # validation du user id 
        if phone_number is None or "":
            raise serializers.ValidationError("Phone number is None or Empty")
        else:
            request=self.context.get('request')
            if request and request.method == "POST":
                # validation de l'existance
                email_exists=Agent.objects.filter(email=email).exists()
                if email_exists:
                    raise serializers.ValidationError("Agent with mail exists")
                else:
                    names_exists=Agent.objects.filter(names=names).exists()
                    if names_exists:
                        raise serializers.ValidationError("Agent with names exists")
                    else:
                        phone_number_exists=Agent.objects.filter(phone_number=phone_number).exists()
                        if phone_number_exists:
                            raise serializers.ValidationError("Agent with phone number exists")
            elif request and request.method == "PUT":
                pk=self.context.get('request').parser_context.get('kwargs').get('pk')  
                # validation de l'existance
                email_exists=Agent.objects.filter(email=email).exists()
                if email_exists:
                    email_exists=Agent.objects.filter(Q(email=email) & Q(id=pk)).exists()
                    if not email_exists:
                        raise serializers.ValidationError("Agent with Mail Exists")
                else:
                    names_exists=Agent.objects.filter(names=names).exists()
                    if names_exists:
                        names_exists=Agent.objects.filter(Q(names=names) & Q(id=pk)).exists()
                        if not names_exists:
                            raise serializers.ValidationError("Agent with Names Exists")
                    else:
                        phone_number_exists=Agent.objects.filter(phone_number=phone_number).exists()
                        if phone_number_exists:
                            phone_number_exists=Agent.objects.filter(Q(phone_number=phone_number) & Q(id=pk)).exists()
                            if not phone_number_exists:
                                raise serializers.ValidationError("Agent with Phone number Exists")              
        return attrs
        
    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}
    
    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        return Agent.objects.create(**validated_data)

class AgentStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
    agent_id = serializers.CharField(write_only=True, allow_null=False, allow_blank=False)

    class Meta:
        fields=[ 'pk', 'email', 'names', 'is_active', 'date_add', 'date_update']

    def validate(self, attrs):
        is_active = attrs.get('is_active')
        agent_id = attrs.get('agent_id')

        if is_active is None or "":
            raise serializers.ValidationError("The Status is None or Empty")
        if agent_id is None or "":
            raise serializers.ValidationError("Agent is None or Empty")
        else:
            agent_exists = Agent.objects.filter(id=agent_id).exists()
            if agent_exists:
                # on recuper l'user courament connecter
                agent = Agent.objects.get(id=agent_id)
                agent.is_active = is_active
                agent.save()
            else:
                raise serializers.ValidationError("Agent is Not Register")
            return attrs
# Profile
class ProfileSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    agent_id = serializers.CharField(write_only=True, allow_null=False, allow_blank=False)
    agent=serializers.SerializerMethodField(read_only=True)
    kind=serializers.CharField(max_length=25)
    adress=serializers.CharField(max_length=255)
    picture=serializers.ImageField(read_only=True)
    picture64 = serializers.CharField(write_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model=Profile
        fields=['pk', 'user', 'agent_id', 'agent', 'kind', 'adress', 'picture', 'picture64', 'date_add', 'date_update']
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1
    
    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        agent_id = attrs.get('agent_id')
        kind = attrs.get('kind')
        
        # validation du kind 
        if kind is None or "":
            raise serializers.ValidationError("Kind is None or Empty")
        # validation du user id 
        if agent_id is None or "":
            raise serializers.ValidationError("Agent is None or Empty")
        else:
            # validation de l'existance de l'user 
            agent_exists=Agent.objects.filter(id=agent_id).exists()
            if not agent_exists:
                raise serializers.ValidationError("Agent is None or not Register")
            else:
                request=self.context.get('request')
                if request and request.method == "POST":
                    # validation de l'existance de l'user dans le profile
                    agent_profile_exists=Profile.objects.filter(agent_id=agent_id).exists()
                    if agent_profile_exists:
                        raise serializers.ValidationError("Agent with Id Exists in Profile")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}

    def get_agent(self, obj):
        return{'pk':obj.agent.pk, 'names':obj.agent.names, 'email':obj.agent.email, 'is_active':obj.agent.is_active, 'phone_number':str(obj.agent.phone_number)}

    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        # on supprimer certains elements du dict
        validated_data.pop('agent_id')
        validated_data.pop('picture64')
        return Profile.objects.create(**validated_data)
# Fonction  
class FunctionSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    wording=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)

    class Meta:
        model=Function
        fields=['pk', 'user', 'wording', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(FunctionSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1
    
    def validate(self, attrs):
        # recuperation des donnees
        wording = attrs.get('wording')

        # validation du wording 
        if wording is None or "":
            raise serializers.ValidationError("Wording is None or Empty")
        else:
            request=self.context.get('request')
            if request and request.method == "POST":
                # validation de l'existance de la function
                function_exists=Function.objects.filter(wording__iexact=wording).exists()
                if function_exists:
                    raise serializers.ValidationError("Wording Exists")
            elif request and request.method == "PUT":
                pk=self.context.get('request').parser_context.get('kwargs').get('pk')
                # validation de l'existance de la function
                function_exists=Function.objects.filter(wording__iexact=wording).exists()
                if function_exists:
                    function_exists=Function.objects.filter(Q(wording__iexact=wording) & Q(id=pk)).exists()
                    if not function_exists:
                        raise serializers.ValidationError("Wording Exists")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}

    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        return Function.objects.create(**validated_data)
# Assignement
class AssignmentSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    agent_id = serializers.CharField(write_only=True, allow_null=False, allow_blank=False)
    agent=serializers.SerializerMethodField(read_only=True)
    function_id = serializers.CharField(write_only=True)
    function=serializers.SerializerMethodField(read_only=True)
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()

    class Meta:
        model=Assignment
        fields=['pk', 'user', 'agent_id', 'agent', 'function_id', 'function', 'date_start', 'date_end', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(AssignmentSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1

    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        agent_id = attrs.get('agent_id')
        function_id = attrs.get('function_id')
        date_start = attrs.get('date_start')
        date_end = attrs.get('date_end')

        # validation du function_id 
        if function_id is None or "":
            raise serializers.ValidationError("Function is None or Empty")
        else:
            function_exists = Function.objects.filter(id=function_id).exists()
            if not function_exists:
                raise serializers.ValidationError("Function is Not Register")
        # validation du user_id 
        if agent_id is None or "":
            raise serializers.ValidationError("Agent is None or Empty")
        else:
            agent_exists = Agent.objects.filter(id=agent_id).exists()
            if not agent_exists:
                raise serializers.ValidationError("Agent is Not Register")
        # validation du date_start 
        if date_start is None or "":
            raise serializers.ValidationError("Starting Date is None or Empty")
        # validation du user_id 
        if date_end is None or "":
            raise serializers.ValidationError("Ending date is None or Empty")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}
    
    def get_agent(self, obj):
        return{'pk':obj.agent.pk, 'names':obj.agent.names, 'email':obj.agent.email, 'is_active':obj.agent.is_active, 'phone_number':str(obj.agent.phone_number)}

    def get_function(self, obj):
        return{'pk':obj.function.pk, 'names':obj.function.wording}

    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        # on supprimer certains elements du dict
        validated_data.pop('agent_id')
        validated_data.pop('function_id')
        return Assignment.objects.create(**validated_data)
# Rate ou taux  
class RateSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    value = serializers.DecimalField(max_digits=13, decimal_places=4, allow_null=False)
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()

    class Meta:
        model=Rate
        fields=['pk', 'user', 'value', 'date_start', 'date_end', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(RateSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1

    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        value = attrs.get('value')

        # validation du function_id 
        if value is None or "":
            raise serializers.ValidationError("Value is None or Empty")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}
    
    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        return Rate.objects.create(**validated_data)

class RateSalarySerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    value = serializers.DecimalField(max_digits=13, decimal_places=4, allow_null=False)
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()
    salary=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Rate
        fields=['pk', 'user', 'value', 'salary', 'date_start', 'date_end', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(RateSalarySerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1

    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        value = attrs.get('value')

        # validation du function_id 
        if value is None or "":
            raise serializers.ValidationError("Value is None or Empty")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}

    def get_salary(self, obj):
        pk=self.context.get('request').parser_context.get('kwargs').get('pk')
        station_id=self.context.get('request').parser_context.get('kwargs').get('station_id')

        parcel_by_agent = Parcel.objects.filter(agent_id=pk, station_id=station_id)
        nbr = parcel_by_agent.count()
        salary = (obj.value * nbr) / 100
        return{'value':str(salary)}

    def create(self, validated_data):
        return Rate.objects.create(**validated_data)
# Satation  
class StationSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    wording = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)

    class Meta:
        model=Station
        fields=['pk', 'user', 'wording', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(StationSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1

    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        wording = attrs.get('wording')

        # validation du function_id 
        if wording is None or "":
            raise serializers.ValidationError("Wording is None or Empty")
        else:
            request=self.context.get('request')
            if request and request.method == "POST":
                # validation de l'existance
                wording_exists=Station.objects.filter(wording__iexact=wording).exists()
                if wording_exists:
                    raise serializers.ValidationError("Wording Exists")
            elif request and request.method == "PUT":
                pk=self.context.get('request').parser_context.get('kwargs').get('pk')
                # validation de l'existance
                wording_exists=Station.objects.filter(wording__iexact=wording).exists()
                if wording_exists:
                    wording_exists=Station.objects.filter(Q(wording__iexact=wording) & Q(id=pk)).exists()
                    if not wording_exists:
                        raise serializers.ValidationError("Wording Exists")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}
    
    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        return Station.objects.create(**validated_data)
# uSAGE  
class UsageSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    wording = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)

    class Meta:
        model=Usage
        fields=['pk', 'user', 'wording', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(UsageSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1

    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        wording = attrs.get('wording')

        # validation du function_id 
        if wording is None or "":
            raise serializers.ValidationError("Wording is None or Empty")
        else:
            request=self.context.get('request')
            if request and request.method == "POST":
                # validation de l'existance
                wording_exists=Usage.objects.filter(wording__iexact=wording).exists()
                if wording_exists:
                    raise serializers.ValidationError("Wording Exists")
            elif request and request.method == "PUT":
                pk=self.context.get('request').parser_context.get('kwargs').get('pk')
                # validation de l'existance
                wording_exists=Usage.objects.filter(wording__iexact=wording).exists()
                if wording_exists:
                    wording_exists=Usage.objects.filter(Q(wording__iexact=wording) & Q(id=pk)).exists()
                    if not wording_exists:
                        raise serializers.ValidationError("Wording Exists")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}
    
    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        return Usage.objects.create(**validated_data)
# Satation  
class Buy_ModeSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    wording = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)

    class Meta:
        model=Buy_Mode
        fields=['pk', 'user', 'wording', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(Buy_ModeSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1

    # Validating data
    def validate(self, attrs):
        # recuperation des donnees
        wording = attrs.get('wording')

        # validation du function_id 
        if wording is None or "":
            raise serializers.ValidationError("Wording is None or Empty")
        else:
            request=self.context.get('request')
            if request and request.method == "POST":
                # validation de l'existance
                wording_exists=Buy_Mode.objects.filter(wording__iexact=wording).exists()
                if wording_exists:
                    raise serializers.ValidationError("Wording Exists")
            elif request and request.method == "PUT":
                pk=self.context.get('request').parser_context.get('kwargs').get('pk')
                # validation de l'existance
                wording_exists=Buy_Mode.objects.filter(wording__iexact=wording).exists()
                if wording_exists:
                    wording_exists=Buy_Mode.objects.filter(Q(wording__iexact=wording) & Q(id=pk)).exists()
                    if not wording_exists:
                        raise serializers.ValidationError("Wording Exists")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}
    
    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        return Buy_Mode.objects.create(**validated_data)