from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TalentViewSet, SimpleLoginView , LogoutView , UserProfileView , LocalisationViewSet , LangueViewSet , CompetenceViewSet

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AgentViewSet, ContactViewSet, CategorieTalentViewSet, TalentViewSet, PhotoViewSet,
    LocalisationViewSet, LangueViewSet, CompetenceViewSet, TalentCompetenceViewSet,
    TypeExperienceViewSet, ExperienceViewSet, TalentAttributViewSet, MediaViewSet
)

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'categories-talents', CategorieTalentViewSet)
router.register(r'talents', TalentViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'localisations', LocalisationViewSet)
router.register(r'langues', LangueViewSet)
router.register(r'competences', CompetenceViewSet)
router.register(r'talent-competences', TalentCompetenceViewSet)
router.register(r'types-experience', TypeExperienceViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'talent-attributs', TalentAttributViewSet)
router.register(r'medias', MediaViewSet)

urlpatterns = [
    path('auth/login/', SimpleLoginView.as_view(), name='api_login'),
     path('auth/logout/', LogoutView.as_view(), name='api_logout'),
      #path('auth/user/', CurrentUserView.as_view(), name='current_user'),
         path('auth/user/', UserProfileView.as_view(), name='user_profile'),
    # ... autres endpoints personnalisés
    # Ajoute toutes les routes du router DRF :
    path('', include(router.urls)),
]
