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



from django.utils.text import slugify
# Modèle Talent
from django.db import models

class Talent(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    photo_principale = models.ImageField(upload_to='talents/photos/', null=True, blank=True)
    taille = models.CharField(max_length=20, blank=True)
    poids = models.CharField(max_length=20, blank=True)
    permis = models.CharField(max_length=20, blank=True)

    slug = models.SlugField(unique=True, max_length=300, blank=True)
    localisations = models.ManyToManyField('Localisation', blank=True)
    langues = models.ManyToManyField('Langue', blank=True)
    competences = models.ManyToManyField('Competence', through='TalentCompetence', blank=True)


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
   

class Localisation(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Langue(models.Model):
    nom = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50, blank=True)  # ex: bilingue, notions

    def __str__(self):
        return f"{self.nom} ({self.niveau})" if self.niveau else self.nom

class Competence(models.Model):
    nom = models.CharField(max_length=150)
    categorie = models.CharField(max_length=100, blank=True)  # ex: danse, chant, instrument

    def __str__(self):
        return self.nom

class TalentCompetence(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=50, blank=True)  # ex: professionnel, débutant
    details = models.TextField(blank=True)

    class Meta:
        unique_together = ('talent', 'competence')

class Experience(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='experiences')
    annee = models.CharField(max_length=20, blank=True)  # ex: 2023, 2022-2024
    titre = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    role = models.CharField(max_length=150, blank=True)
    type_experience = models.CharField(max_length=100, blank=True)  # ex: film, publicité, théâtre

    def __str__(self):
        return f"{self.annee} - {self.titre}"

class TalentAttribut(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='attributs')
    cle = models.CharField(max_length=100)
    valeur = models.TextField(blank=True)

    class Meta:
        unique_together = ('talent', 'cle')

class Media(models.Model):
    class MediaType(models.TextChoices):
        PHOTO = "photo", "Photo"
        VIDEO = "video", "Vidéo"

    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='medias')
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    fichier = models.FileField(upload_to='talents/media/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.talent.nom} - {self.media_type} - {self.id}"
    
class Contact(models.Model):
    class ContactType(models.TextChoices):
        EMAIL = "email", "Email"
        TELEPHONE = "telephone", "Téléphone"
        LINKEDIN = "linkedin", "LinkedIn"
        TWITTER = "twitter", "Twitter"
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        AUTRE = "autre", "Autre"

    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='contacts')
    type_contact = models.CharField(max_length=20, choices=ContactType.choices)
    valeur = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)  # optionnel, ex: "Pro perso", "Pro"

    def __str__(self):
        return f"{self.talent.nom} - {self.get_type_contact_display()}: {self.valeur}"
    
    
    
class Actualite(models.Model):
    TITRE_MAX_LENGTH = 250
    TYPE_CHOICES = [
        ('actualite', 'Actualité Générale'),
        ('interview', 'Interview'),
        ('article', 'Article'),
        ('communique', 'Communiqué de Presse'),
    ]

    titre = models.CharField(max_length= 250 ,verbose_name="Titre de l'actualité")
    slug = models.SlugField(unique=True, max_length= 500, verbose_name="Slug (URL propre)", help_text="Un identifiant unique pour l'URL, généré à partir du titre.")
    type_actualite = models.CharField(max_length=20, choices=TYPE_CHOICES, default='actualite', verbose_name="Type d'actualité")
    contenu = models.TextField(verbose_name="Contenu de l'actualité")
    date_publication = models.DateTimeField(default=timezone.now, verbose_name="Date de publication")
    image_principale = models.ImageField(upload_to='actualites/images/', null=True, blank=True, verbose_name="Image principale")
    talent_associe = models.ForeignKey('Talent', on_delete=models.SET_NULL, null=True, blank=True, related_name='actualites', verbose_name="Talent associé (optionnel)")
    est_publie = models.BooleanField(default=True, verbose_name="Publiée sur le site")

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-date_publication'] # Ordonner les actualités par date de publication décroissante

    def __str__(self):
        return self.titre    
    
    
class ProjetArtistique(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('pre_production', 'Pré-production'),
        ('en_developpement', 'En développement'),
        ('annule', 'Annulé'),
    ]
    TYPE_CHOICES = [
        ('film', 'Film'),
        ('serie', 'Série TV'),
        ('theatre', 'Théâtre'),
        ('publicite', 'Publicité'),
        ('court_metrage', 'Court-métrage'),
        ('web_serie', 'Web-série'),
        ('autre', 'Autre'),
    ]

    titre = models.CharField(max_length=250, verbose_name="Titre du projet")
    description = models.TextField(blank=True, verbose_name="Description du projet")
    type_projet = models.CharField(max_length=50, choices=TYPE_CHOICES, default='autre', verbose_name="Type de projet")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours', verbose_name="Statut du projet")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date de début")
    date_fin_prevue = models.DateField(null=True, blank=True, verbose_name="Date de fin prévue")
    date_fin_reelle = models.DateField(null=True, blank=True, verbose_name="Date de fin réelle")
    image_principale = models.ImageField(upload_to='projets/images/', null=True, blank=True, verbose_name="Image du projet")
    liens_externes = models.URLField(max_length=500, blank=True, verbose_name="Lien externe (ex: site officiel, bande-annonce)")
    talents = models.ManyToManyField('Talent', related_name='projets_artistiques', blank=True, verbose_name="Talents impliqués")

    class Meta:
        verbose_name = "Projet Artistique"
        verbose_name_plural = "Projets Artistiques"
        ordering = ['-date_debut', 'titre']

    def __str__(self):
        return self.titre
    
    
    
class Evenement(models.Model):
    TYPE_CHOICES = [
        ('festival', 'Festival'),
        ('ceremonie_prix', 'Cérémonie de Prix'),
        ('projection', 'Projection Spéciale'),
        ('autre', 'Autre Événement'),
    ]

    nom = models.CharField(max_length=250, verbose_name="Nom de l'événement")
    type_evenement = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre', verbose_name="Type d'événement")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin (si applicable)")
    lieu = models.CharField(max_length=250, blank=True, verbose_name="Lieu de l'événement")
    description = models.TextField(blank=True, verbose_name="Description de l'événement")
    liens_externes = models.URLField(max_length=500, blank=True, verbose_name="Lien externe (ex: site officiel)")
    talents_participants = models.ManyToManyField('Talent', related_name='evenements_participes', blank=True, verbose_name="Talents participants")
    projets_associes = models.ManyToManyField('ProjetArtistique', related_name='evenements_associes', blank=True, verbose_name="Projets associés (ex: sélection officielle)")

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date_debut']

    def __str__(self):
        return self.nom
    