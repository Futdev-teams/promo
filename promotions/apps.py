from django.apps import AppConfig


from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils import timezone

def archiver_promotions(sender, **kwargs):
    from .models import Produit
    Produit.objects.filter(
        date_fin_promo__lte=timezone.now(),
        est_expire=False
    ).update(est_expire=True)

class PromotionsConfig(AppConfig):
    name = 'promotions'

    def ready(self):
        post_migrate.connect(archiver_promotions, sender=self)