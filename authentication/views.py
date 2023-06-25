import django
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from . serializers import (
    SendPasswordResetEmailSerializer, 
    UserChangePasswordSerializer, 
    UserLoginSerializer, 
    UserStatusSerializer,
    UserPasswordResetSerializer, 
    UserRegistrationSerializer, 
    UserListSerializer,
    ProfileSerializer
)
from django.contrib.auth import authenticate
from . renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
# importation des models
from . models import User, Profile
# importation de la permission personnaliser sur base du type
from . permissions import IsStaffPermissions
from django.contrib.auth import logout
import uuid
from base64 import b64decode
from django.core.files.base import ContentFile
from gaci_security_api.pagination import NoLimitResultsPagination
from .mixins import QSFilterWithByUserLogged

# json
from django.core import serializers
# import du jwt pour la gestion de token
from rest_framework_simplejwt.views import (
    TokenVerifyView # token de verification
)
from . serializers import CustomTokenVerifySerializer

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_data_for_user(user):
    # recup data
    user_auth = User.objects.filter(email=user.email)
    # convert data to json
    user_auth_list = serializers.serialize('json', user_auth)
    return {
        'user_auth': user_auth_list,
    }

# decode base64 to image
def add_photo(image_base64):
    extension = image_base64.split(';')[0].split('/')[1]
    base64 = image_base64.split(',')[1]
    image_data = b64decode(base64)
    image_name = str(uuid.uuid4())+"." + extension
    photo_image = ContentFile(image_data, image_name)
    return photo_image

# custom viwa to verify token
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer

# Starting User 
class UserNoStaffRegistrationViewMSCM(APIView):

    renderer_classes = [UserRenderer] # le rendu de la vue

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # on verifie si le staff est true
        data = serializer.validated_data
        lst = list(data.items())
        staff = lst[5][1]
        if staff == True:
            return Response({'msg':'This Link is Unauthorized To Create Staff User'}, status=status.HTTP_201_CREATED)
        else:
            user = serializer.save()
            # on prepare le return
            token = get_tokens_for_user(user)
            data = get_data_for_user(user)
            return Response({'token':token, 'data':data, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserStaffRegistrationViewMSCM(APIView):

    renderer_classes = [UserRenderer] # le rendu de la vue

    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # on prepare le return
        token = get_tokens_for_user(user)
        data = get_data_for_user(user)
        return Response({'token':token, 'data':data, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            token = get_tokens_for_user(user)
            data = get_data_for_user(user)
            return Response({'token':token, 'data':data, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':'Email or Password is not Valid'}}, status=status.HTTP_404_NOT_FOUND)

class UserLogoutView(APIView):
    renderer_classes = [UserRenderer]

    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        if user is not None:
            logout(request)
            return Response({'msg':'Logout Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Logout Error'})

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]

    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]    
    
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class UserChangeStatusView(APIView):
    renderer_classes = [UserRenderer]

    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]    
    
    def post(self, request, format=None):
        serializer = UserStatusSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Status Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


# Starting list data user
# Lister une seul enregistrement
class UserDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserListSerializer

# lister et creer au meme moment
class UserListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination 

    queryset = User.objects.all()
    serializer_class = UserListSerializer
# Ending User


# Starting Profile
# Lister un seul enregistrement sur base de son user_id
class ProfileUserIdDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    lookup_field = 'user_id'

class ProfileUserLoggedListView(
    QSFilterWithByUserLogged,
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    # pagination_class = NoLimitResultsPagination  
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
# Lister une seul enregistrement
class ProfileDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# lister et creer au meme moment
class ProfileListCreateView(
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')

        # definition de l'img en base64
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, picture=picture)

# mise en jour 
class ProfileUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    lookup_field = 'pk'
    
    # on creer une methode pour jouer avec les donnes de facon individuel
    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')

        # definition de l'img en base64
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, picture=picture)

# suppression
class ProfileDeleteView(
    generics.DestroyAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    

    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except django.db.models.deletion.ProtectedError as e:
            return Response(status=status.HTTP_423_LOCKED, data={'detail':str(e)})
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        instance.delete()
# Ending Profile