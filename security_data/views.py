import django
from authentication.renderers import UserRenderer
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Want_To_Research, Curfew_And_Instability, Population_Alert, Recognized
from rest_framework.views import APIView
from authentication.permissions import IsStaffModelPermissions
from gaci_security_api.pagination import NoLimitResultsPagination
# l'importe l'objet Q pour faciliter apartir de plusieurs champs
from django.db.models import Q
from .serializers import(
    Want_To_ResearchSerializer, 
    Curfew_And_InstabilitySerializer, 
    Population_AlertSerializer
)
from django.contrib.auth import get_user_model
# UserQuerySetMixin permet de filter les resultats sur base des permissions
from authentication.mixins import(
    QSFilterWithByUserLogged
)
import cv2
from .simple_facerec import SimpleFacerec

User = get_user_model()

import uuid
from base64 import b64decode
from django.core.files.base import ContentFile

# Create your views here.
# decode base64 to image
def add_photo(image_base64):
    extension = image_base64.split(';')[0].split('/')[1]
    base64 = image_base64.split(',')[1]
    image_data = b64decode(base64)
    image_name = str(uuid.uuid4())+"." + extension
    photo_image = ContentFile(image_data, image_name)
    return photo_image

# Starting Want_To_Research
# Lister une seul enregistrement
class Want_To_ResearchDetailView(
    generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Want_To_Research.objects.all()
    serializer_class = Want_To_ResearchSerializer

# Lister tous
class Want_To_ResearchIsFinishListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Want_To_Research.objects.filter(is_finish='1')
    serializer_class = Want_To_ResearchSerializer  

class Want_To_ResearchIsCancelListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    # pagination_class = NoLimitResultsPagination  

    queryset = Want_To_Research.objects.filter(is_cancel='1')
    serializer_class = Want_To_ResearchSerializer     

class Want_To_ResearchInProgressListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    # pagination_class = NoLimitResultsPagination  

    queryset = Want_To_Research.objects.filter(Q(is_finish='0') & Q(is_cancel='0'))
    serializer_class = Want_To_ResearchSerializer  
    
# Lister pour l'user connected et creer au meme moment
class Want_To_ResearchListCreateView(
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffModelPermissions]

    queryset = Want_To_Research.objects.all()
    serializer_class = Want_To_ResearchSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')
        # debut de verification et modification
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, picture=picture)

# mise en jour 
class Want_To_ResearchUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Want_To_Research.objects.all()
    serializer_class = Want_To_ResearchSerializer

    lookup_field = 'pk'

    # gerer
    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')
        # debut de verification et modification
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, picture=picture)

# suppression
class Want_To_ResearchDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffModelPermissions]

    queryset = Want_To_Research.objects.all()
    serializer_class = Want_To_ResearchSerializer

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
# Ending Want_To_Research


# Starting Curfew_And_Instability
# Lister une seul enregistrement
class Curfew_And_InstabilityDetailView(
    generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Curfew_And_Instability.objects.all()
    serializer_class = Curfew_And_InstabilitySerializer

# Lister tous
class Curfew_And_InstabilityIsFinishListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Curfew_And_Instability.objects.filter(is_finish='1')
    serializer_class = Curfew_And_InstabilitySerializer  

class Curfew_And_InstabilityIsCancelListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Curfew_And_Instability.objects.filter(is_cancel='1')
    serializer_class = Curfew_And_InstabilitySerializer     

class Curfew_And_InstabilityInProgressListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    pagination_class = NoLimitResultsPagination  

    queryset = Curfew_And_Instability.objects.filter(Q(is_finish='0') & Q(is_cancel='0'))
    serializer_class = Curfew_And_InstabilitySerializer  
    
# Lister pour l'user connected et creer au meme moment
class Curfew_And_InstabilityListCreateView(
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffModelPermissions]

    queryset = Curfew_And_Instability.objects.all()
    serializer_class = Curfew_And_InstabilitySerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')
        # debut de verification et modification
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, picture=picture)

# mise en jour 
class Curfew_And_InstabilityUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffModelPermissions]

    queryset = Curfew_And_Instability.objects.all()
    serializer_class = Curfew_And_InstabilitySerializer

    lookup_field = 'pk'

    # gerer
    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'image en base64
        picture64 = serializer.validated_data.get('picture64')
        # debut de verification et modification
        if picture64 is None or picture64 == "":
            picture = None
        else:
            picture = add_photo(picture64)
        serializer.save(user=user, picture=picture)

# suppression
class Curfew_And_InstabilityDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffModelPermissions]

    queryset = Curfew_And_Instability.objects.all()
    serializer_class = Curfew_And_InstabilitySerializer

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
# Ending Curfew_And_Instability


# Starting Population_Alert
# Lister une seul enregistrement
class Population_AlertDetailView(
    generics.RetrieveAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Population_Alert.objects.all()
    serializer_class = Population_AlertSerializer

# Lister tous
class Population_AlertIsFinishListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    # pagination_class = NoLimitResultsPagination  

    queryset = Population_Alert.objects.filter(is_finish='1')
    serializer_class = Population_AlertSerializer  

class Population_AlertIsCancelListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    # pagination_class = NoLimitResultsPagination  

    queryset = Population_Alert.objects.filter(is_cancel='1')
    serializer_class = Population_AlertSerializer     

class Population_AlertInProgressListView(
    generics.ListAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated]

    # gestion de page
    # pagination_class = NoLimitResultsPagination  

    queryset = Population_Alert.objects.filter(Q(is_finish='0') & Q(is_cancel='0'))
    serializer_class = Population_AlertSerializer  
    
# Lister pour l'user connected et creer au meme moment
class Population_AlertListCreateView(
    generics.ListCreateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated,]

    queryset = Population_Alert.objects.all()
    serializer_class = Population_AlertSerializer

    # gerer
    def perform_create(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        serializer.save(user=user)

# mise en jour 
class Population_AlertUpdateView(
    generics.UpdateAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffModelPermissions]

    queryset = Population_Alert.objects.all()
    serializer_class = Population_AlertSerializer

    lookup_field = 'pk'

    # gerer
    def perform_update(self, serializer):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        # on recupere l'image en base64
        serializer.save(user=user)

# suppression
class Population_AlertDeleteView(
    generics.DestroyAPIView):

    renderer_classes = [UserRenderer] # le rendu de la vue
    # on l'authentication
    authentication_classes = [JWTAuthentication]
    # on gere les permissions pour cette view (acces, ...)
    permission_classes = [permissions.IsAuthenticated, IsStaffModelPermissions]

    queryset = Population_Alert.objects.all()
    serializer_class = Population_AlertSerializer

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
# Ending Population_Alert


# code pour les views qui vont faire le streming
# code pour verifier la correspondance faciale et retourner une reponse
# lister etcreer au meme moment
class Try_RecognitionRunACheckListCreateView(APIView):

    renderer_classes = [UserRenderer] # le rendu de la vue

    def post(self, request, format=None):
        # var portant le nombre de tentative de reconnaisance
        iterations = 0
        results = '' # recevrant toute les chaines de reponses de la reconnaissance
        data=request.data
        if len(data) <= 0:
            return Response({'msg':'Url is not Null or Empty'}, status=status.HTTP_201_CREATED)
        else:
            # on recupere l'obj du wtr
            wtr_exists = Want_To_Research.objects.filter(pk=data['id']).exists()
            if not wtr_exists:
                return Response({'msg':'Id is not Null or Empty'}, status=status.HTTP_201_CREATED)
            else:
                wtr = Want_To_Research.objects.get(pk=data['id'])
                # le noms de correspondance trouver
                names = ''
                # on verifie si on reconnaisance ...
                type = ''
                if(data['type'] == 'wtr'):
                    type = 'media/Images/Datasource/Wtr/'
                elif(data['type'] == 'cai'):
                    type = 'media/Images/Datasource/Cai/'
                    
                # Encode faces from a folder
                sfr = SimpleFacerec()
                sfr.load_encoding_images(f"{type}")

                cap = cv2.VideoCapture(0)
                
                # code pour les cameras sur reseau
                # url = f"http://{data['url']}/video"
                # cap.open(url)

                while True:
                    iterations = iterations + 1
                    ret, frame = cap.read()

                    # Detection des faces
                    face_locations, face_names = sfr.detect_known_faces(frame)
                    for face_loc, name in zip(face_locations, face_names):
                        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                        cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

                    cv2.imshow("Frame", frame)
                    
                    # verification de correspondance
                    if len(face_names) <= 0 :
                        results = results + f'Pas des correspondance trouvé {str(face_names)}...\n'
                        print(f'Pas des correspondance trouvé {str(face_names)}...')
                    else:
                        names = str(face_names)
                        results = results + f'Correspondance trouvé {str(face_names)}...\n'
                        print(f'Correspondance trouvé {str(face_names)}...')
                                            
                    cv2.waitKey(1)
                    # on arret le streaming....
                    if iterations == 200:
                        break

                cap.release()
                cv2.destroyAllWindows()   
                
                # Vérifier si la sous-chaine se trouve dans la chaine principale 
                if "Correspondance trouvé" in results:
                    print ('Sous-chaîne trouvée')
                    # on enregistre
                    obj = Recognized.objects.create(wtr=wtr, names=names, longitude=data['longitude'], latittude=data['latittude'])
                    if obj is None:
                        print('Obj is not Register')
                    else:
                        print('Obj is Register')
                else:
                    print('Sous-chaîne non trouvée')
                return Response({'msg':'Fin de l\'iterration', 'results': results}, status=status.HTTP_201_CREATED)