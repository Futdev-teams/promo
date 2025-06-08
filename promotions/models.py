from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import secrets
import random
import string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models
from django.urls import reverse

from django.db import models
from django.urls import reverse

class Entreprise(models.Model):
    nom = models.CharField(max_length=100)
    categorie_e = models.CharField(max_length=50, choices=[
        ('Hôtel', 'Hôtel'),
        ('Supermarché', 'Supermarché'), 
        ('hôpital', 'Hôpital'),
        ('magasin', 'Magasin'),
        ('réseau', 'Réseau'),
    ], default="Supermarché")
    email = models.EmailField()
    description = models.TextField(default="Soyez à l'afflux de nos meilleurs promos")
    contact = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='logos/')
    banniere = models.ImageField(upload_to='bannieres/')
    localisation = models.CharField(max_length=255, help_text="Adresse textuelle pour l'affichage")
    localisation_map = models.TextField(help_text="Texte pour l'iframe Google Maps (ex: '6.1234,1.5678' ou 'Nom+du+lieu')")
    latitude = models.FloatField(blank=True, null=True,default=0)
    longitude = models.FloatField(blank=True, null=True,default=0)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True, help_text="Description pour le référencement SEO")
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Mots-clés pour le référencement SEO, séparés par des virgules")
    
    # Statistiques d'abonnés
    abonnes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('entreprise_public_view', kwargs={'entreprise_id': self.id})
    
    def get_map_url(self):
        """Génère l'URL Google Maps à partir de localisation_map"""
        if ',' in self.localisation_map:
            # Si c'est des coordonnées lat,long
            return f"https://maps.google.com/maps?q={self.localisation_map}&z=15&output=embed"
        else:
            # Si c'est une adresse textuelle
            return f"https://maps.google.com/maps?q={self.localisation_map.replace(' ', '+')}&z=15&output=embed"
    
    def update_coordinates(self):
        """Méthode pour mettre à jour latitude/longitude à partir de localisation_map"""
        # Ici vous pourriez intégrer une API Google Maps pour géocoder l'adresse
        pass

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        
        if 'username' not in extra_fields:
            extra_fields['username'] = email
        
        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    entreprise = models.OneToOneField(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True)
    password_reset_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserAccountManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def generate_verification_code(self):
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.verification_expiration = timezone.now() + timezone.timedelta(minutes=10)
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            temp_password = secrets.token_urlsafe(10)
            self.set_password(temp_password)
            self.send_credentials(temp_password)
        super().save(*args, **kwargs)
    
    def send_credentials(self, temp_password):
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        subject = 'Vos identifiants de connexion'
        message = f"""
        Bonjour,
        
        Voici vos identifiants temporaires:
        Email: {self.email}
        Mot de passe temporaire: {temp_password}
        
        Connectez-vous ici: {site_url}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )

class VerificationToken(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timezone.timedelta(minutes=10)

class Categorie(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promotionnel = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut_promo = models.DateTimeField()
    date_fin_promo = models.DateTimeField()
    quantite = models.IntegerField(default=1)
    image = models.ImageField(upload_to='produits/', default='produits/inconnues.jpg')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    est_expire = models.BooleanField(default=False)
    def is_promo_active(self):
        now = timezone.now()
        return self.date_debut_promo <= now <= self.date_fin_promo and not self.est_expire

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.date_fin_promo < now:
            self.est_expire = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    @property
    def discount_percentage(self):
        return round(((self.prix - self.prix_promotionnel) / self.prix) * 100, 2)

class HoraireOuverture(models.Model):
    JOURS_SEMAINE = [
        ('LUN', 'Lundi'),
        ('MAR', 'Mardi'),
        ('MER', 'Mercredi'),
        ('JEU', 'Jeudi'),
        ('VEN', 'Vendredi'),
        ('SAM', 'Samedi'),
        ('DIM', 'Dimanche'),
    ]
    
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='horaires_ouverture')
    jour = models.CharField(max_length=3, choices=JOURS_SEMAINE)
    heure_ouverture = models.TimeField(null=True, blank=True)
    heure_fermeture = models.TimeField(null=True, blank=True)
    est_ferme = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['jour']
        unique_together = ['entreprise', 'jour']

class AvisClient(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='avis_clients')
    nom = models.CharField(max_length=100)
    note = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-date_creation']

class FAQ(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    reponse = models.TextField()
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']

class ImageEntreprise(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='entreprise_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image pour {self.entreprise.nom}"
    


class ProductView(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='views')
    date = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, choices=[
        ('direct', 'Direct'),
        ('qr', 'QR Code'),
        ('social', 'Réseau social'),
        ('email', 'Email'),
        ('other', 'Autre')
    ])
    device = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Vue de {self.produit.nom} le {self.date}"
    

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Produit

@receiver(pre_save, sender=Produit)
def check_promo_expiration(sender, instance, **kwargs):
    if instance.date_fin_promo and instance.date_fin_promo < timezone.now():
        instance.est_expire = True
    else:
        instance.est_expire = False


class ActivityLog(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
  

# models.py
from django.db import models
from django.core.validators import validate_email

class EmailAbonne(models.Model):
    email = models.EmailField(unique=True, validators=[validate_email])
    code_verification = models.CharField(max_length=6)
    est_verifie = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class AbonnementEntreprise(models.Model):
    email = models.ForeignKey(EmailAbonne, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    date_abonnement = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('email', 'entreprise')