from rest_framework import serializers
from .models import Talent
from .models import Localisation, Langue, Competence
from rest_framework import serializers
from .models import Talent, Localisation, Langue, Competence, TalentCompetence, Experience, TalentAttribut, Media, Contact

# serializers.py
from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_joined']


class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = ['id', 'nom']

class LangueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Langue
        fields = ['id', 'nom', 'niveau']

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id', 'nom', 'categorie']

class TalentCompetenceSerializer(serializers.ModelSerializer):
    competence = CompetenceSerializer()
    class Meta:
        model = TalentCompetence
        fields = ['id', 'competence', 'niveau', 'details']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'annee', 'titre', 'description', 'role', 'type_experience']

class TalentAttributSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentAttribut
        fields = ['id', 'cle', 'valeur']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'media_type', 'fichier', 'description']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'type_contact', 'valeur', 'description']

class TalentSerializer(serializers.ModelSerializer):
    localisations = LocalisationSerializer(many=True, read_only=True)
    langues = LangueSerializer(many=True, read_only=True)
    competences = TalentCompetenceSerializer(source='talentcompetence_set', many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    attributs = TalentAttributSerializer(many=True, read_only=True)
    medias = MediaSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = [
            'id', 'nom', 'date_naissance', 'slug','description', 'photo_principale',
            'taille', 'poids', 'permis',
            'localisations', 'langues', 'competences', 'experiences',
            'attributs', 'medias', 'contacts'
        ]
