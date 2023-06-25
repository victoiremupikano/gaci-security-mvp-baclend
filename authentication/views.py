import django
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import pagination
from cadastre.pagination import NoLimitResultsPagination
from rest_framework.views import APIView
from . serializers import (
    SendPasswordResetEmailSerializer, 
    UserChangePasswordSerializer, 
    UserLoginSerializer, 
    UserStatusSerializer,
    UserPasswordResetSerializer, 
    UserRegistrationSerializer, 
    AgentSerializer,
    AgentStatusSerializer,
    ProfileSerializer, 
    FunctionSerializer, 
    AssignmentSerializer,
    UserListSerializer,
    RateSerializer,
    RateSalarySerializer,
    StationSerializer,
    UsageSerializer,
    Buy_ModeSerializer
)
from django.contrib.auth import authenticate
from . renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
# importation des models
from . models import User, Agent, Profile, Function, Assignment, Rate, Station, Usage, Buy_Mode
# importation de la permission personnaliser sur base du type
from . permissions import IsStaffPermissions
from django.contrib.auth import logout
import uuid
from base64 import b64decode
from django.core.files.base import ContentFile

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
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
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

# Starting Agent
# Lister une seul enregistrement
class AgentDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]
    
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

# lister tous
class AgentListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

# changer le status de l'agent
class AgentChangeStatusView(APIView):
    renderer_classes = [UserRenderer]

    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]    
    
    def post(self, request, format=None):
        serializer = AgentStatusSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Status Changed Successfully'}, status=status.HTTP_200_OK)

# lister et creer au meme moment
class AgentListCreateView(
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# mise en jour 
class AgentUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    lookup_field = 'pk'
    
    # on creer une methode pour jouer avec les donnes de facon individuel
    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# suppression
class AgentDeleteView(
    generics.DestroyAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer    

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
# rps
# lister tous agents actifs
class AgentListActifView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Agent.objects.filter(is_active="1")
    serializer_class = AgentSerializer

# lister tous agents actifs
class AgentListNoActifView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Agent.objects.filter(is_active="0")
    serializer_class = AgentSerializer
# Ending Agent

# Starting Profile
# Lister une seul enregistrement
class ProfileDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# lister et creer au meme moment
class ProfileListCreateView(
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'id de l'agent
        agent_id = serializer.validated_data.get('agent_id')
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')

        # debut de verification et modification
        agent = Agent.objects.get(id=agent_id)
        # definition de l'img en base64
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, agent=agent, picture=picture)

# mise en jour 
class ProfileUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    lookup_field = 'pk'
    
    # on creer une methode pour jouer avec les donnes de facon individuel
    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'id de l'agent
        agent_id = serializer.validated_data.get('agent_id')
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')

        # debut de verification et modification
        agent = Agent.objects.get(id=agent_id)
        # definition de l'img en base64
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, agent=agent, picture=picture)

# suppression
class ProfileDeleteView(
    generics.DestroyAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

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

# Starting Function
# Lister une seul enregistrement
class FunctionDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]
    
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

# lister tous
class FunctionListView(
    generics.ListAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

# lister et creer au meme moment
class FunctionListCreateView(
    generics.ListCreateAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# mise en jour 
class FunctionUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

    lookup_field = 'pk'

    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# suppression
class FunctionDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

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
# Ending Function

# Starting Assignment
# Lister une seul enregistrement
class AssignmentDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

# Lister une seul enregistrement apartir de agent id
class AssignmentDetailIdAgentView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    lookup_field = 'agent_id'

# lister et creer au meme moment 
class AssignmentListCreateView(
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'id de l'user
        agent_id = serializer.validated_data.get('agent_id')
        # on recupere le function_id
        function_id = serializer.validated_data.get('function_id')
        # debut de verification et modification
        # si exists on recuper les objets
        agent = Agent.objects.get(id=agent_id)
        function = Function.objects.get(id=function_id)
        serializer.save(user=user, agent=agent, function=function)

# lister tous
class AssignmentListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

# mise en jour 
class AssignmentUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    lookup_field = 'pk'

    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'id de l'user
        agent_id = serializer.validated_data.get('agent_id')
        # on recupere le function_id
        function_id = serializer.validated_data.get('function_id')
        # debut de verification et modification
        # si exists on recuper les objets
        agent = Agent.objects.get(id=agent_id)
        function = Function.objects.get(id=function_id)
        serializer.save(user=user, agent=agent, function=function)

# suppression
class AssignmentDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

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
# Ending Function

# Starting Rate
# Lister une seul enregistrement
class RateDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]
    
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

# lister tous
class RateListView(
    generics.ListAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination 

    queryset = Rate.objects.all()
    serializer_class = RateSerializer

# lister et creer au meme moment
class RateListCreateView(
    generics.ListCreateAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Rate.objects.all()
    serializer_class = RateSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# lister tous les rates en y appliquant les tot des parcels lotis par un agent
class RateListView(
    generics.ListAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination

    queryset = Rate.objects.all()
    serializer_class = RateSalarySerializer

# mise en jour 
class RateUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Rate.objects.all()
    serializer_class = RateSerializer

    lookup_field = 'pk'

    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# suppression
class RateDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Rate.objects.all()
    serializer_class = RateSerializer

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
# Ending Rate

# Starting Station
# Lister une seul enregistrement
class StationDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]
    
    queryset = Station.objects.all()
    serializer_class = StationSerializer

# lister tous
class StationListView(
    generics.ListAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Station.objects.all()
    serializer_class = StationSerializer

# lister et creer au meme moment
class StationListCreateView(
    generics.ListCreateAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Station.objects.all()
    serializer_class = StationSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# mise en jour 
class StationUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Station.objects.all()
    serializer_class = StationSerializer

    lookup_field = 'pk'

    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# suppression
class StationDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Station.objects.all()
    serializer_class = StationSerializer

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
# Ending Station

# Starting Usage
# Lister une seul enregistrement
class UsageDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]
    # gestion de page
    pagination_class = [pagination.PAGE_BREAK]

    queryset = Usage.objects.all()
    serializer_class = UsageSerializer

# lister tous
class UsageListView(
    generics.ListCreateAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Usage.objects.all()
    serializer_class = UsageSerializer

# lister et creer au meme moment
class UsageListCreateView(
    generics.ListCreateAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Usage.objects.all()
    serializer_class = UsageSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# mise en jour 
class UsageUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Usage.objects.all()
    serializer_class = UsageSerializer

    lookup_field = 'pk'

    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# suppression
class UsageDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Usage.objects.all()
    serializer_class = UsageSerializer

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
# Ending Usage

# Starting Buy_Mode
# Lister une seul enregistrement
class Buy_ModeDetailView(generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]
    
    queryset = Buy_Mode.objects.all()
    serializer_class = Buy_ModeSerializer

# lister tous
class Buy_ModeListView(
    generics.ListAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    # gestion de page
    pagination_class = NoLimitResultsPagination  
    
    queryset = Buy_Mode.objects.all()
    serializer_class = Buy_ModeSerializer

# lister et creer au meme moment
class Buy_ModeListCreateView(
    generics.ListCreateAPIView):
    
    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Buy_Mode.objects.all()
    serializer_class = Buy_ModeSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# mise en jour 
class Buy_ModeUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Buy_Mode.objects.all()
    serializer_class = Buy_ModeSerializer

    lookup_field = 'pk'

    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# suppression
class Buy_ModeDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffPermissions]

    queryset = Buy_Mode.objects.all()
    serializer_class = Buy_ModeSerializer

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
# Ending Buy_Mode 