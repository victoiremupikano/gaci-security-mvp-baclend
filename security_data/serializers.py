from rest_framework import serializers
from . models import Want_To_Research, Curfew_And_Instability, Population_Alert
#l'importe l'objet Q pour faciliter apartir de plusieurs champs
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class Want_To_ResearchSerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    names=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    kind=serializers.CharField(max_length=25, allow_null=True, allow_blank=True)
    is_finish=serializers.BooleanField(default=False)
    is_cancel=serializers.BooleanField(default=False)
    reason=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    picture=serializers.ImageField(read_only=True)
    picture64 = serializers.CharField(write_only=True, allow_null=True, allow_blank=True)
   
    class Meta:
        model=Want_To_Research
        fields=['pk', 'user', 'names', 'kind', 'is_finish', 'is_cancel', 'reason', 'picture', 'picture64', 'date_add', 'date_update']
    
    def __init__(self, *args, **kwargs):
        super(Want_To_ResearchSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1
    
    def validate(self, attrs):
        names = attrs.get('names')

        request=self.context.get('request')
        if request and request.method == "POST":
            # verfication
            if names is None or "":
                raise serializers.ValidationError("Names is None or Empty")
        elif request and request.method == "PUT":
            pk=self.context.get('request').parser_context.get('kwargs').get('pk')
            # verfication
            names_exists = Want_To_Research.objects.filter(names=names).exists()
            if names_exists:
                names_exists = Want_To_Research.objects.filter(Q(names=names) & Q(id=pk) & Q(is_finish='1')).exists()
                if not names_exists:
                    raise serializers.ValidationError("Want_To_Research with Names Exists")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}

    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        # on supprimer certains elements du dict
        validated_data.pop('picture64')
        return Want_To_Research.objects.create(**validated_data)
       
class Curfew_And_InstabilitySerializer(serializers.ModelSerializer):
    # creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    reason=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    longitude=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    latittude=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    is_finish=serializers.BooleanField(default=False)
    is_cancel=serializers.BooleanField(default=False)
    picture=serializers.ImageField(read_only=True)
    picture64 = serializers.CharField(write_only=True, allow_null=True, allow_blank=True)
    
    class Meta:
        model=Curfew_And_Instability
        fields=['pk', 'user', 'reason', 'longitude', 'latittude', 'is_finish', 'is_cancel', 'picture', 'picture64', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(Curfew_And_InstabilitySerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1
    
    def validate(self, attrs):
        reason = attrs.get('reason')
        longitude = attrs.get('longitude')
        latittude = attrs.get('latittude')

        if reason is None or "":
            raise serializers.ValidationError("Reason is None or Empty")
        if longitude is None or "":
            raise serializers.ValidationError("Longitude is None or Empty")
        if latittude is None or "":
            raise serializers.ValidationError("Latitude is None or Empty")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}

    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        # on supprimer certains elements du dict
        validated_data.pop('picture64')
        return Curfew_And_Instability.objects.create(**validated_data)
    
class Population_AlertSerializer(serializers.ModelSerializer):
# creation d'un ne se trouvant pas dans le model
    user=serializers.SerializerMethodField(read_only=True)
    reason_issued=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    reason_to_certify=serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    longitude=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    latittude=serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    is_finish=serializers.BooleanField(default=False)
    is_cancel=serializers.BooleanField(default=False)
    
    class Meta:
        model=Population_Alert
        fields=['pk', 'user', 'reason_issued', 'reason_to_certify', 'longitude', 'latittude', 'is_finish', 'is_cancel', 'date_add', 'date_update']

    def __init__(self, *args, **kwargs):
        super(Population_AlertSerializer, self).__init__(*args, **kwargs)
        request=self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == "GET":
            self.Meta.depth = 1
    
    def validate(self, attrs):
        reason_issued = attrs.get('reason_issued')
        longitude = attrs.get('longitude')
        latittude = attrs.get('latittude')

        if reason_issued is None or "":
            raise serializers.ValidationError("Reason is None or Empty")
        if longitude is None or "":
            raise serializers.ValidationError("Longitude is None or Empty")
        if latittude is None or "":
            raise serializers.ValidationError("Latitude is None or Empty")
        return attrs

    # methode pour retourner l'obj du cle etranger
    def get_user(self, obj):
        return{'pk':obj.user.pk, 'names':obj.user.names, 'email':obj.user.email, 'is_active':obj.user.is_active, 'phone_number':str(obj.user.phone_number)}

    # on cree une surchage de create car email n y appartient pas ou on peux le faire dans la vue
    def create(self, validated_data):
        return Population_Alert.objects.create(**validated_data)