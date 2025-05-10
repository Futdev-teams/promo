from django.urls import path # type: ignore
from . import views
from django.http import HttpResponse

urlpatterns = [
    # Page d'accueil
    path('', views.accueil, name='accueil'),

    #page de la liste des entrerprise :
    path('entreprise', views.entreprise ,name='entreprise'),

    # Page de détail d'une entreprise
    path('entreprise/<int:entreprise_id>/', views.entreprise_detail, name='entreprise_detail'),

    # Page de contact
    path('contact/', views.contact, name='contact'),

    # Page des archives
    path('archives/', views.archives, name='archives'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    # Inscription
    #path('inscription/', views.inscription, name='inscription'),

    # Connexion
    path('connexion/', views.user_login, name='connexion'),

    #Reset_password
    #path('reset_password',views.resetpassword, name='password_reset'),

    #path('mon-compte/', views.gestion_entreprise, name='gestion_entreprise'),
    path('ajouter-promotion/', views.ajouter_promotion, name='ajouter_promotion'),
    path('modifier-promotion/<int:produit_id>/', views.modifier_promotion, name='modifier_promotion'),
    path('supprimer-promotion/<int:produit_id>/', views.supprimer_promotion, name='supprimer_promotion'),


    path('signup/', views.demande_inscription, name='signup'),
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
    path('resend_verification_code/<int:user_id>/',views.resend_verification_code, name='resend_verification_code'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('modifier-votre-informations/', views.modifier_vos_informations, name='modifier_informations'),
    path('modifier-mot-de-passe/', views.modifier_votre_mot_de_passe, name='modifier_mot_de_passe'),
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    
    # Dashboard entreprise
    path('dashboard_entreprise/', views.dashboard_entreprise, name='dashboard_entreprise'),
    
    path('mon-entreprise/', views.dashboard_entreprise, name='dashboard_entreprise'),
    path('mon-entreprise/ajouter-promotion/', views.ajouter_promotion, name='ajouter_promotion'),
    path('mon-entreprise/modifier-promotion/<int:pk>/', views.modifier_promotion, name='modifier_promotion'),
    path('mon-entreprise/supprimer-promotion/<int:pk>/', views.supprimer_promotion, name='supprimer_promotion'),
    
    # Vue publique de l'entreprise
    path('entreprise/<int:pk>/', views.entreprise_public_view, name='entreprise_public_view'),
    
    # Gestion des promotions (API)
    path('api/promotions/', views.PromotionListCreate.as_view(), name='promotion-list-create'),
    path('api/promotions/<int:pk>/', views.PromotionRetrieveUpdateDestroy.as_view(), name='promotion-retrieve-update-destroy'),
    path('profile/', views.profile, name='profile'),
    path('demande-inscription/', views.demande_inscription, name='demande_inscription'),



    path('favicon.ico', lambda request: HttpResponse(status=204)),


    #path("admin/users/", views.user_dashboard, name="user_dashboard"),
    #path("admin/users/create/", views.create_user, name="create_user"),
    #path("admin/users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
]
