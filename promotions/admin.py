
# Register your models here.
from django.contrib import admin # type: ignore
from . models import *
from.models import Utilisateur
admin.site.register(Categorie)
admin.site.register(Entreprise)
admin.site.register(Produit)
# Register your models here.
from django.contrib import admin
from . models import *
# Register your models here.


# Register your models here.

@admin.register(Utilisateur)
class UniversalAdmin(admin.ModelAdmin):

    search_fields       = ('first_name', 'email','is_admin' )
    exclude = ('password',)

    #def get_list_display(self, request):
    #    return [field.name for field in self.model._meta.concrete_fields]

    def get_list_display(self, request):

        #list_name = [field.name for field in self.model._meta.concrete_fields]
        list_display = [field.name for field in self.model._meta.concrete_fields]

        return list_display

from django.apps import AppConfig

class PromotionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promotions'


class LoginConfig(AppConfig):
    name = 'login'

    