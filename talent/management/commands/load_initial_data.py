import json
from django.core.management.base import BaseCommand
from talent.models import (
    Agent, CategorieTalent, Localisation, Langue, Competence,
    Talent, TypeExperience, Experience, TalentAttribut
)

class Command(BaseCommand):
    help = "Charge des données initiales dans la base depuis un fichier JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Chemin vers le fichier JSON contenant les données',
            default='talent/data/initial_data.json',
        )

    def filter_model_fields(self, model, data_dict):
        model_fields = set(f.name for f in model._meta.get_fields())
        return {k: v for k, v in data_dict.items() if k in model_fields}

    def handle(self, *args, **options):
        file_path = options['file']
        self.stdout.write(f"Chargement des données depuis {file_path}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Charger Agents
        agents_map = {}
        for agent_data in data.get('agents', []):
            filtered_data = self.filter_model_fields(Agent, agent_data)
            agent, created = Agent.objects.get_or_create(
                email=filtered_data['email'],
                defaults=filtered_data
            )
            if not created:
                for k, v in filtered_data.items():
                    setattr(agent, k, v)
                agent.save()
            agents_map[agent.email] = agent
            self.stdout.write(f"{'Créé' if created else 'Existant'} agent : {agent}")

        # Charger Categories Talents
        categories_map = {}
        for cat_data in data.get('categories_talents', []):
            cat, created = CategorieTalent.objects.get_or_create(nom=cat_data['nom'])
            categories_map[cat.nom] = cat
            self.stdout.write(f"{'Créée' if created else 'Existante'} catégorie : {cat.nom}")

        # Charger Localisations
        localisations_map = {}
        for loc_data in data.get('localisations', []):
            loc, created = Localisation.objects.get_or_create(nom=loc_data['nom'])
            localisations_map[loc.nom] = loc
            self.stdout.write(f"{'Créée' if created else 'Existante'} localisation : {loc.nom}")

        # Charger Langues
        langues_map = {}
        for lang_data in data.get('langues', []):
            lang, created = Langue.objects.get_or_create(
                nom=lang_data['nom'],
                niveau=lang_data.get('niveau', '')
            )
            langues_map[lang.nom] = lang
            self.stdout.write(f"{'Créée' if created else 'Existante'} langue : {lang.nom}")

        # Charger Compétences
        competences_map = {}
        for comp_data in data.get('competences', []):
            comp, created = Competence.objects.get_or_create(
                nom=comp_data['nom'],
                defaults={'categorie': comp_data.get('categorie', '')}
            )
            competences_map[comp.nom] = comp
            self.stdout.write(f"{'Créée' if created else 'Existante'} compétence : {comp.nom}")

        # Charger Types d'expérience
        types_exp_map = {}
        for type_exp_data in data.get('type_experiences', []):
            type_exp, created = TypeExperience.objects.get_or_create(nom=type_exp_data['nom'])
            types_exp_map[type_exp.nom] = type_exp
            self.stdout.write(f"{'Créé' if created else 'Existant'} type d'expérience : {type_exp.nom}")

        # Charger Talents
        for talent_data in data.get('talents', []):
            agent_email = talent_data.pop('agent_email', None)
            categories_names = talent_data.pop('categories', [])
            localisations_names = talent_data.pop('localisations', [])
            langues_names = talent_data.pop('langues', [])
            competences_names = talent_data.pop('competences', [])
            experiences_data = talent_data.pop('experiences', [])
            attributs_data = talent_data.pop('attributs', [])

            filtered_talent_data = self.filter_model_fields(Talent, talent_data)

            agent = agents_map.get(agent_email) if agent_email else None
            if agent:
                filtered_talent_data['agent'] = agent

            talent, created = Talent.objects.get_or_create(
                nom=filtered_talent_data['nom'],
                prenom=filtered_talent_data.get('prenom', ''),
                defaults=filtered_talent_data
            )
            if not created:
                for k, v in filtered_talent_data.items():
                    setattr(talent, k, v)
                talent.agent = agent
                talent.save()

            # Relations ManyToMany
            talent.categories.set([categories_map[name] for name in categories_names if name in categories_map])
            talent.localisations.set([localisations_map[name] for name in localisations_names if name in localisations_map])
            talent.langues.set([langues_map[name] for name in langues_names if name in langues_map])
            talent.competences.set([competences_map[name] for name in competences_names if name in competences_map])

            # Supprimer les expériences existantes avant recréation
            talent.experiences.all().delete()
            for exp_data in experiences_data:
                type_exp_obj = None
                type_exp_nom = exp_data.get('type_experience')
                if type_exp_nom and type_exp_nom in types_exp_map:
                    type_exp_obj = types_exp_map[type_exp_nom]
                Experience.objects.create(
                    talent=talent,
                    annee=exp_data.get('annee', ''),
                    titre=exp_data.get('titre', ''),
                    description=exp_data.get('description', ''),
                    role=exp_data.get('role', ''),
                    type_experience=type_exp_obj
                )

            # Supprimer attributs existants et recréer
            talent.attributs.all().delete()
            for attr_data in attributs_data:
                TalentAttribut.objects.create(
                    talent=talent,
                    cle=attr_data.get('cle', ''),
                    valeur=attr_data.get('valeur', '')
                )

            self.stdout.write(f"{'Créé' if created else 'Mis à jour'} talent : {talent}")

        self.stdout.write(self.style.SUCCESS("Chargement des données terminé."))

