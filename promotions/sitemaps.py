from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Entreprise, Produit, FAQ

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'a_propos', 'contact']  # Assure-toi que ces noms correspondent à tes URLs nommées

    def location(self, item):
        return reverse(item)

class EntrepriseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Entreprise.objects.filter(est_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

class ProduitSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Produit.objects.filter(est_actif=True, entreprise__est_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

class FAQSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return FAQ.objects.all()

    def location(self, obj):
        return reverse('faq_detail', kwargs={'pk': obj.pk})  # Adapte si tu as un slug
