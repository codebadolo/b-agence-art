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


from rest_framework import serializers
from .models import (
    Agent, Contact, CategorieTalent, Talent, Photo,
    Localisation, Langue, Competence, TalentCompetence,
    TypeExperience, Experience, TalentAttribut, Media
)

# Serializer pour Contact (lié à Agent)
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'type_contact', 'valeur', 'description']

# Serializer pour Agent avec contacts imbriqués
class AgentSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Agent
        fields = [
            'id', 'nom', 'prenom', 'email', 'telephone', 'adresse', 'agence',
            'site_web', 'linkedin', 'facebook', 'instagram', 'notes', 'contacts'
        ]

# Serializer simple pour CategorieTalent
class CategorieTalentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieTalent
        fields = ['id', 'nom']

# Serializer simple pour Localisation
class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = ['id', 'nom']

# Serializer simple pour Langue
class LangueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Langue
        fields = ['id', 'nom', 'niveau']

# Serializer simple pour Competence
class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id', 'nom', 'categorie']

# Serializer pour TalentCompetence (relation intermédiaire)
class TalentCompetenceSerializer(serializers.ModelSerializer):
    competence = CompetenceSerializer(read_only=True)
    competence_id = serializers.PrimaryKeyRelatedField(
        queryset=Competence.objects.all(), source='competence', write_only=True
    )

    class Meta:
        model = TalentCompetence
        fields = ['id', 'competence', 'competence_id', 'niveau', 'details']

# Serializer pour TypeExperience
class TypeExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeExperience
        fields = ['id', 'nom']

# Serializer pour Experience
class ExperienceSerializer(serializers.ModelSerializer):
    type_experience = TypeExperienceSerializer(read_only=True)
    type_experience_id = serializers.PrimaryKeyRelatedField(
        queryset=TypeExperience.objects.all(), source='type_experience', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Experience
        fields = ['id', 'annee', 'titre', 'description', 'role', 'type_experience', 'type_experience_id']

# Serializer pour TalentAttribut
class TalentAttributSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentAttribut
        fields = ['id', 'cle', 'valeur']

# Serializer pour Media
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'media_type', 'fichier', 'description']

# Serializer pour Photo (galerie)
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'description']

# Serializer principal pour Talent
class TalentSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), source='agent', write_only=True, allow_null=True, required=False
    )
    localisations = LocalisationSerializer(many=True, read_only=True)
    localisations_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Localisation.objects.all(), source='localisations', write_only=True, required=False
    )
    langues = LangueSerializer(many=True, read_only=True)
    langues_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Langue.objects.all(), source='langues', write_only=True, required=False
    )
    competences = TalentCompetenceSerializer(source='talentcompetence_set', many=True, required=False)
    categories = CategorieTalentSerializer(many=True, read_only=True)
    categories_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CategorieTalent.objects.all(), source='categories', write_only=True, required=False
    )
    experiences = ExperienceSerializer(many=True, read_only=True)
    attributs = TalentAttributSerializer(many=True, read_only=True)
    medias = MediaSerializer(many=True, read_only=True)
    galerie_photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = [
            'id', 'nom', 'prenom', 'sexe', 'date_naissance', 'description', 'photo_principale',
            'taille', 'poids', 'permis', 'slug', 'agent', 'agent_id',
            'localisations', 'localisations_ids',
            'langues', 'langues_ids',
            'competences',
            'categories', 'categories_ids',
            'experiences', 'attributs', 'medias', 'galerie_photos',
        ]

    def create(self, validated_data):
        # Extraire les relations ManyToMany write_only
        localisations = validated_data.pop('localisations', [])
        langues = validated_data.pop('langues', [])
        categories = validated_data.pop('categories', [])
        agent = validated_data.pop('agent', None)

        talent = Talent.objects.create(agent=agent, **validated_data)

        if localisations:
            talent.localisations.set(localisations)
        if langues:
            talent.langues.set(langues)
        if categories:
            talent.categories.set(categories)

        return talent

    def update(self, instance, validated_data):
        localisations = validated_data.pop('localisations', None)
        langues = validated_data.pop('langues', None)
        categories = validated_data.pop('categories', None)
        agent = validated_data.pop('agent', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if agent is not None:
            instance.agent = agent
        instance.save()

        if localisations is not None:
            instance.localisations.set(localisations)
        if langues is not None:
            instance.langues.set(langues)
        if categories is not None:
            instance.categories.set(categories)

        return instance
