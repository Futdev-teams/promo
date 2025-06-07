from django.urls import path # type: ignore
from . import views
from . import api_views 
from django.http import HttpResponse

urlpatterns = [
    # Page d'accueil
    path('', views.accueil, name='accueil'),

    #page de la liste des entrerprise :
    path('entreprise', views.entreprise ,name='entreprise'),

    # Page de détail d'une entreprise
    # path('public/<int:entreprise_id>/', views.entreprise_detail, name='entreprise_detail'),


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
    #path('ajouter-promotion/', views.ajouter_promotion, name='ajouter_promotion'),
    #path('modifier-promotion/<int:produit_id>/', views.modifier_promotion, name='modifier_promotion'),
    #path('supprimer-promotion/<int:produit_id>/', views.supprimer_promotion, name='supprimer_promotion'),


    path('signup/', views.demande_inscription, name='signup'),
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
    path('resend_verification_code/<int:user_id>/',views.resend_verification_code, name='resend_verification_code'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('modifier-votre-informations/', views.modifier_vos_informations, name='modifier_informations'),
    path('modifier-mot-de-passe/', views.modifier_votre_mot_de_passe, name='modifier_mot_de_passe'),
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    
    # Dashboard entreprise
    #path('dashboard_entreprise/', views.dashboard_entreprise, name='dashboard_entreprise'),
    
    #path('mon-entreprise/', views.dashboard_entreprise, name='dashboard_entreprise'),
    #path('mon-entreprise/ajouter-promotion/', views.ajouter_promotion, name='ajouter_promotion'),
    #path('mon-entreprise/modifier-promotion/<int:pk>/', views.modifier_promotion, name='modifier_promotion'),
    #path('mon-entreprise/supprimer-promotion/<int:pk>/', views.supprimer_promotion, name='supprimer_promotion'),
    
    # Vue publique de l'entreprise
    #path('entreprise/<int:pk>/', views.entreprise_public_view, name='entreprise_public_view'),
    
    # Gestion des promotions (API)
    #path('api/promotions/', views.PromotionListCreate.as_view(), name='promotion-list-create'),
    #path('api/promotions/<int:pk>/', views.PromotionRetrieveUpdateDestroy.as_view(), name='promotion-retrieve-update-destroy'),
    path('profile/', views.profile, name='profile'),
    path('demande-inscription/', views.demande_inscription, name='demande_inscription'),
    path('images/add/', views.add_entreprise_image, name='add_entreprise_image'),
    path('images/delete/<int:pk>/', views.delete_entreprise_image, name='delete_entreprise_image'),

    # Gestion abonnés
    #path('abonnes/add/', login_required(views.add_abonne), name='add_abonne'),
    #path('abonnes/delete/<int:pk>/', login_required(views.delete_abonne), name='delete_abonne'),

    # Vue publique
    path('dashboard/', views.dashboard, name='dashboard'),
    path('entreprise/<int:entreprise_id>/', views.entreprise_public_view, name='entreprise_public_view'),
    path('dashboard/', views.dashboard, name='dashboard_entreprise'),
    # Gestion de l'entreprise
    path('entreprise/modifier/', views.modifier_entreprise, name='modifier_entreprise'),
    
    # Gestion des promotions
    path('promotion/ajouter/', views.ajouter_promotion, name='ajouter_promotion'),
    path('promotion/<int:produit_id>/modifier/', views.modifier_promotion, name='modifier_promotion'),
    path('promotion/<int:produit_id>/supprimer/', views.supprimer_promotion, name='supprimer_promotion'),
    path('dashboard/produits/<int:product_id>/reactivate/', views.reactivate_product, name='reactivate_product'),
    
    # Gestion des horaires
    path('entreprise/<int:entreprise_id>/hours/', views.update_hours, name='update_hours'),
    
    # Gestion des avis
    path('dashboard/reviews/<int:review_id>/approve/', views.approve_review, name='approve_review'),
    path('dashboard/reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    
    # Gestion de la FAQ
    path('dashboard/entreprise/<int:entreprise_id>/faq/add/', views.add_faq, name='add_faq'),
    path('dashboard/faq/<int:faq_id>/edit/', views.edit_faq, name='edit_faq'),
    path('dashboard/faq/<int:faq_id>/delete/', views.delete_faq, name='delete_faq'),
    path('promotions-actives/', views.promotions_actives, name='promotions_actives'),
    # Export des données
    path('export/', views.export_data, name='export_data'),
    path('about_me/',views.propos,name='propos_view'),
    path('api/abonnement-email/<int:entreprise_id>/', views.abonnement_par_entreprise, name='abonnement_email'),
    path('api/confirmer-code/', views.confirmer_code_verification, name='confirmer_code'),
    path('api/promo-notif/<int:entreprise_id>/', views.check_promo_notification, name='check_promo_notification'),













    path('favicon.ico', lambda request: HttpResponse(status=204)),

    path('api/entreprise/<int:entreprise_id>/horaires/', api_views.entreprise_horaires, name='api_entreprise_horaires'),
    #path('api/avis/<int:avis_id>/approve/', api_views.approve_avis, name='api_approve_avis'),
    #path('api/faq/', api_views.faq_list, name='api_faq_list'),
    #path('api/faq/<int:faq_id>/', api_views.faq_detail, name='api_faq_detail'),
    #path('api/produits/<int:produit_id>/status/', api_views.update_produit_status, name='api_update_produit_status'),
    #path("admin/users/", views.user_dashboard, name="user_dashboard"),
    #path("admin/users/create/", views.create_user, name="create_user"),
    #path("admin/users/delete/<int:user_id>/", views.delete_user, name="delete_user"),




    # URLs pour l'administration
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_user_management, name='admin_user_management'),
    path('admin-dashboard/users/create/', views.admin_create_user, name='admin_create_user'),
    path('admin-dashboard/users/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('admin-dashboard/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-dashboard/users/<int:user_id>/assign-entreprise/', views.admin_assign_entreprise, name='admin_assign_entreprise'),
    path('admin-dashboard/entreprises/', views.admin_entreprise_management, name='admin_entreprise_management'),
    path('admin-dashboard/entreprises/create/', views.admin_create_entreprise, name='admin_create_entreprise'),
    path('admin-dashboard/entreprises/<int:entreprise_id>/edit/', views.admin_edit_entreprise, name='admin_edit_entreprise'),
    path('admin-dashboard/entreprises/<int:entreprise_id>/delete/', views.admin_delete_entreprise, name='admin_delete_entreprise'),
    path('admin-dashboard/promotions/', views.admin_promotion_management, name='admin_promotion_management'),


]
