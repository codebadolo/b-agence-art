import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est requis')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email



from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Agent, représentant un agent d'artiste
class Agent(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=50, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    agence = models.CharField(max_length=255, blank=True)
    site_web = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom else self.nom

# Contacts liés à un agent (pas au talent)
class Contact(models.Model):
    class ContactType(models.TextChoices):
        EMAIL = "email", "Email"
        TELEPHONE = "telephone", "Téléphone"
        LINKEDIN = "linkedin", "LinkedIn"
        TWITTER = "twitter", "Twitter"
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        AUTRE = "autre", "Autre"

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='contacts')
    type_contact = models.CharField(max_length=20, choices=ContactType.choices)
    valeur = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.agent} - {self.get_type_contact_display()}: {self.valeur}"

# Catégories de talents (ex : Comédien, Réalisateur)
class CategorieTalent(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

# Talent
class Talent(models.Model):
    SEXE_CHOICES = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150, blank=True)
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    photo_principale = models.ImageField(upload_to='talents/photos/', null=True, blank=True)
    taille = models.CharField(max_length=20, blank=True)
    poids = models.CharField(max_length=20, blank=True)
    permis = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(unique=True, max_length=300, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name='talents')

    localisations = models.ManyToManyField('Localisation', blank=True)
    langues = models.ManyToManyField('Langue', blank=True)
    competences = models.ManyToManyField('Competence', through='TalentCompetence', blank=True)
    categories = models.ManyToManyField(CategorieTalent, blank=True, related_name='talents')

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.prenom} {self.nom}" if self.prenom else self.nom
            slug_candidate = slugify(base)
            slug = slug_candidate
            n = 1
            while Talent.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{slug_candidate}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom else self.nom

# Galerie de photos pour un talent
class Photo(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='galerie_photos')
    image = models.ImageField(upload_to='talents/galerie/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Photo de {self.talent}"

# Localisation
class Localisation(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Langue
class Langue(models.Model):
    nom = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.niveau})" if self.niveau else self.nom

# Compétence
class Competence(models.Model):
    nom = models.CharField(max_length=150)
    categorie = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom

# Relation Talent-Competence avec infos complémentaires
class TalentCompetence(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=50, blank=True)
    details = models.TextField(blank=True)

    class Meta:
        unique_together = ('talent', 'competence')

# Type d'expérience (ex : Théâtre, Cinéma, Publicité)
class TypeExperience(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

# Expérience professionnelle d’un talent
class Experience(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='experiences')
    annee = models.CharField(max_length=20, blank=True)
    titre = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    role = models.CharField(max_length=150, blank=True)
    type_experience = models.ForeignKey(TypeExperience, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.annee} - {self.titre}"

# Attributs personnalisés d’un talent
class TalentAttribut(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='attributs')
    cle = models.CharField(max_length=100)
    valeur = models.TextField(blank=True)

    class Meta:
        unique_together = ('talent', 'cle')

# Médias liés au talent (photo, vidéo)
class Media(models.Model):
    class MediaType(models.TextChoices):
        PHOTO = "photo", "Photo"
        VIDEO = "video", "Vidéo"

    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='medias')
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    fichier = models.FileField(upload_to='talents/media/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.talent} - {self.media_type} - {self.id}"
