"""
URL configuration for mon_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.contrib.sitemaps.views import sitemap
from promotions.sitemaps import StaticViewSitemap, EntrepriseSitemap, ProduitSitemap, FAQSitemap
sitemaps = {
    'static': StaticViewSitemap(),
    'entreprises': EntrepriseSitemap(),
    'produits': ProduitSitemap(),
    'faq': FAQSitemap(),
}


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # URLs de l'application promotions
    path('', include('promotions.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

# Configuration pour servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

