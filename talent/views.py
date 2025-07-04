from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions
from .models import Talent
from .models import Localisation, Langue, Competence
from .serializers import TalentSerializer  , UserProfileSerializer , LocalisationSerializer, LangueSerializer, CompetenceSerializer

from rest_framework.permissions import IsAuthenticated

'''class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        
        return Response(serializer.data)'''
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            })
        return Response({'error': 'Identifiants invalides'}, status=400)


class SimpleLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'email': user.email}, status=200)
        return Response({'detail': 'Identifiants invalides'}, status=400)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_200_OK)
    
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import (
    Agent, Contact, CategorieTalent, Talent, Photo,
    Localisation, Langue, Competence, TalentCompetence,
    TypeExperience, Experience, TalentAttribut, Media
)
from .serializers import (
    AgentSerializer, ContactSerializer, CategorieTalentSerializer, TalentSerializer, PhotoSerializer,
    LocalisationSerializer, LangueSerializer, CompetenceSerializer, TalentCompetenceSerializer,
    TypeExperienceSerializer, ExperienceSerializer, TalentAttributSerializer, MediaSerializer
)

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'prenom', 'email']

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

class CategorieTalentViewSet(viewsets.ModelViewSet):
    queryset = CategorieTalent.objects.all()
    serializer_class = CategorieTalentSerializer
    permission_classes = [IsAuthenticated]

class TalentViewSet(viewsets.ModelViewSet):
    queryset = Talent.objects.all()
    serializer_class = TalentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['nom', 'prenom', 'slug', 'description']

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

class LocalisationViewSet(viewsets.ModelViewSet):
    queryset = Localisation.objects.all()
    serializer_class = LocalisationSerializer
    permission_classes = [IsAuthenticated]

class LangueViewSet(viewsets.ModelViewSet):
    queryset = Langue.objects.all()
    serializer_class = LangueSerializer
    permission_classes = [IsAuthenticated]

class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [IsAuthenticated]

class TalentCompetenceViewSet(viewsets.ModelViewSet):
    queryset = TalentCompetence.objects.all()
    serializer_class = TalentCompetenceSerializer
    permission_classes = [IsAuthenticated]

class TypeExperienceViewSet(viewsets.ModelViewSet):
    queryset = TypeExperience.objects.all()
    serializer_class = TypeExperienceSerializer
    permission_classes = [IsAuthenticated]

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

class TalentAttributViewSet(viewsets.ModelViewSet):
    queryset = TalentAttribut.objects.all()
    serializer_class = TalentAttributSerializer
    permission_classes = [IsAuthenticated]

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
