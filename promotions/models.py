





from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import secrets

class Entreprise(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='logos/')
    banniere = models.ImageField(upload_to='bannieres/')
    localisation = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.nom

from django.contrib.auth.models import AbstractUser
import random, string


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
        
        # Générer un username automatique si non fourni
        if 'username' not in extra_fields:
            extra_fields['username'] = email  # Ou générez un username unique
        
        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractUser):
    # Supprimez le champ username ou rendez-le non obligatoire
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
    REQUIRED_FIELDS = []  # Retirez 'username' des REQUIRED_FIELDS
    
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
        if not self.pk:  # Création d'un nouvel utilisateur
            temp_password = secrets.token_urlsafe(10)
            self.set_password(temp_password)
            self.send_credentials(temp_password)
        super().save(*args, **kwargs)
    
    from django.conf import settings

    def send_credentials(self, temp_password):
        # Vérifier si SITE_URL est défini
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')  # Valeur par défaut
        
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

from django.utils import timezone
    
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promotionnel = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut_promo = models.DateTimeField()
    date_fin_promo = models.DateTimeField()
    quantite = models.IntegerField(default=1)
    image = models.ImageField(upload_to='produits/', default= 'produits/inconnues.jpg')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0) 
    est_expire = models.BooleanField(default=False, verbose_name="Promo expirée")
    

    def save(self, *args, **kwargs):
        """Met à jour automatiquement est_expire lors de la sauvegarde"""
        if self.date_fin_promo <= timezone.now():
            self.est_expire = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
    @property
    def discount_percentage(self):
        """Calcule le pourcentage de réduction."""
        return round(((self.prix - self.prix_promotionnel) / self.prix) * 100, 2)