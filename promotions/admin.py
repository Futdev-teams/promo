
# Register your models here.
from django.contrib import admin # type: ignore
from . models import *
from.models import Utilisateur
admin.site.register(Categorie)
admin.site.register(Entreprise)
admin.site.register(Produit)
admin.site.register(AvisClient)
admin.site.register(FAQ)
admin.site.register(HoraireOuverture)
# Register your models here.
from django.contrib import admin
from . models import *
# Register your models here.


# Register your models here.


from django.apps import AppConfig

class PromotionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promotions'


class LoginConfig(AppConfig):
    name = 'promotions'
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Utilisateur._meta.fields]
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'is_admin']
    readonly_fields = ['last_login', 'date_joined']  # Optionnel
    list_editable = ['is_active', 'is_staff', 'is_superuser', 'is_admin']  # Modification directe dans la liste
    exclude = ['password']  # ou pas, à toi de voir

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('entreprise')


    