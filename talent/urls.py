from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TalentViewSet, SimpleLoginView , LogoutView , UserProfileView , LocalisationViewSet , LangueViewSet , CompetenceViewSet

router = DefaultRouter()
router.register(r'talents', TalentViewSet)
router.register(r'localisations', LocalisationViewSet)
router.register(r'langues', LangueViewSet)
router.register(r'competences', CompetenceViewSet)
urlpatterns = [
    path('auth/login/', SimpleLoginView.as_view(), name='api_login'),
     path('auth/logout/', LogoutView.as_view(), name='api_logout'),
      #path('auth/user/', CurrentUserView.as_view(), name='current_user'),
         path('auth/user/', UserProfileView.as_view(), name='user_profile'),
    # ... autres endpoints personnalisés
    # Ajoute toutes les routes du router DRF :
    path('', include(router.urls)),
]
