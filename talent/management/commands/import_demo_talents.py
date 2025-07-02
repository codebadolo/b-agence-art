from django.core.management.base import BaseCommand
from talent.models import (
    Talent, Localisation, Langue, Competence, TalentCompetence,
    Experience, TalentAttribut, Media, Contact
)
from django.core.files.base import ContentFile
from talent.demo_talents import DEMO_TALENTS

def get_or_create_localisation(nom):
    return Localisation.objects.get_or_create(nom=nom)[0]

def get_or_create_langue(nom, niveau):
    return Langue.objects.get_or_create(nom=nom, niveau=niveau)[0]

def get_or_create_competence(nom, categorie):
    return Competence.objects.get_or_create(nom=nom, categorie=categorie)[0]

class Command(BaseCommand):
    help = "Charge une vingtaine de talents de démo inspirés d'agence-arcenciel.com"

    def handle(self, *args, **options):
        for data in DEMO_TALENTS:
            talent, created = Talent.objects.get_or_create(
                nom=data["nom"],
                defaults={
                    "prenom": data.get("prenom", ""),
                    "date_naissance": data["date_naissance"],
                    "description": data["description"],
                    "taille": data["taille"],
                    "poids": data["poids"],
                    "permis": data["permis"],
                }
            )
            # Localisations
            for loc_nom in data.get("localisations", []):
                talent.localisations.add(get_or_create_localisation(loc_nom))
            # Langues
            for lang_nom, niveau in data.get("langues", []):
                talent.langues.add(get_or_create_langue(lang_nom, niveau))
            # Compétences
            for comp_nom, niveau, categorie in data.get("competences", []):
                comp = get_or_create_competence(comp_nom, categorie)
                TalentCompetence.objects.get_or_create(
                    talent=talent, competence=comp, defaults={"niveau": niveau}
                )
            # Attributs
            for cle, valeur in data.get("attributs", []):
                TalentAttribut.objects.get_or_create(talent=talent, cle=cle, defaults={"valeur": valeur})
            # Contacts
            for type_contact, valeur, description in data.get("contacts", []):
                Contact.objects.get_or_create(
                    talent=talent, type_contact=type_contact, valeur=valeur, defaults={"description": description}
                )
            # Expériences
            for exp in data.get("experiences", []):
                Experience.objects.get_or_create(
                    talent=talent,
                    annee=exp["annee"],
                    titre=exp["titre"],
                    defaults={
                        "description": exp["description"],
                        "role": exp["role"],
                        "type_experience": exp["type_experience"],
                    }
                )
            # Media de test (photo fictive)
            if not talent.medias.exists():
                Media.objects.create(
                    talent=talent,
                    media_type="photo",
                    fichier=ContentFile(b"fake image", name=f"{talent.nom.lower().replace(' ', '_')}.jpg"),
                    description="Photo de profil (démo)"
                )
            talent.save()
            self.stdout.write(self.style.SUCCESS(f"Talent {'créé' if created else 'mis à jour'} : {talent.nom}"))
