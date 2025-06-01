from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Entreprise, Produit
from django.contrib.auth.forms import UserCreationForm







from .models import Utilisateur
class UserForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'password']

class UserForms(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'password']

class FormulaireDeModificationDuMotDePasse(forms.Form):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}), label="Mot de passe")
    nouveau_mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'}), label="Nouveau mot de passe")
    confirmation_du_nouveau_mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'}), label="Confirmation du nouveau mot de passe")

class FormulaireMotDePasseOublie(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label="Email")




class ConnexionForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']







# forms.py
from django import forms
from .models import Utilisateur

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['email', 'first_name', 'last_name', 'entreprise']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entreprise'].queryset = Entreprise.objects.filter(utilisateur=self.instance)






from django import forms
from django.forms import ModelForm, DateInput, TimeInput
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Entreprise, Produit, HoraireOuverture, FAQ
from datetime import date

class EntrepriseForm(ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom', 'email', 'contact', 'logo', 'banniere', 'localisation', 
                 'latitude', 'longitude', 'facebook', 'instagram', 'twitter', 'website']
        widgets = {
            'localisation': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude < -90 or latitude > 90:
            raise ValidationError("La latitude doit être entre -90 et 90")
        return latitude
    
    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude < -180 or longitude > 180:
            raise ValidationError("La longitude doit être entre -180 et 180")
        return longitude

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput
from django.utils import timezone
import datetime
from .models import Produit

class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'prix_promotionnel', 
                 'date_debut_promo', 'date_fin_promo', 'quantite', 'image', 'categorie']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date_debut_promo': DateInput(attrs={'type': 'date'}),
            'date_fin_promo': DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        prix = cleaned_data.get('prix')
        prix_promotionnel = cleaned_data.get('prix_promotionnel')
        date_debut = cleaned_data.get('date_debut_promo')
        date_fin = cleaned_data.get('date_fin_promo')

        # Conversion en datetime si les champs sont des date simples
        if isinstance(date_debut, datetime.date) and not isinstance(date_debut, datetime.datetime):
            date_debut = datetime.datetime.combine(date_debut, datetime.time.min)
            cleaned_data['date_debut_promo'] = date_debut

        if isinstance(date_fin, datetime.date) and not isinstance(date_fin, datetime.datetime):
            date_fin = datetime.datetime.combine(date_fin, datetime.time.min)
            cleaned_data['date_fin_promo'] = date_fin

        now = timezone.now()

        if prix and prix_promotionnel and prix_promotionnel >= prix:
            raise ValidationError("Le prix promotionnel doit être inférieur au prix normal.")

        if date_debut and date_fin and date_fin < date_debut:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")

        if date_fin and date_fin < now:
            raise ValidationError("La date de fin ne peut pas être dans le passé.")

        return cleaned_data

class HoraireForm(forms.Form):
    JOURS_SEMAINE = HoraireOuverture.JOURS_SEMAINE
    
    def __init__(self, *args, **kwargs):
        horaires_existants = kwargs.pop('horaires', {})
        super().__init__(*args, **kwargs)
        
        for jour in self.JOURS_SEMAINE:
            code_jour = jour[0]
            horaire = horaires_existants.get(code_jour)
            
            self.fields[f'closed_{code_jour}'] = forms.BooleanField(
                label=f'Fermé le {jour[1]}',
                required=False,
                initial=horaire.est_ferme if horaire else False
            )
            
            self.fields[f'open_{code_jour}'] = forms.TimeField(
                label='Heure d\'ouverture',
                required=False,
                widget=TimeInput(attrs={'type': 'time'}),
                initial=horaire.heure_ouverture if horaire and not horaire.est_ferme else None
            )
            
            self.fields[f'close_{code_jour}'] = forms.TimeField(
                label='Heure de fermeture',
                required=False,
                widget=TimeInput(attrs={'type': 'time'}),
                initial=horaire.heure_fermeture if horaire and not horaire.est_ferme else None
            )
    
    def clean(self):
        cleaned_data = super().clean()
        
        for jour in self.JOURS_SEMAINE:
            code_jour = jour[0]
            est_ferme = cleaned_data.get(f'closed_{code_jour}')
            heure_ouverture = cleaned_data.get(f'open_{code_jour}')
            heure_fermeture = cleaned_data.get(f'close_{code_jour}')
            
            if not est_ferme:
                if not heure_ouverture or not heure_fermeture:
                    raise ValidationError(
                        f"Veuillez spécifier les heures d'ouverture et de fermeture pour {jour[1]} ou marquer comme fermé"
                    )
                
                if heure_fermeture <= heure_ouverture:
                    raise ValidationError(
                        f"L'heure de fermeture doit être après l'heure d'ouverture pour {jour[1]}"
                    )
        
        return cleaned_data

class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'reponse', 'ordre']
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'Poser une question fréquente'}),
            'reponse': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Fournir une réponse claire'}),
        }
    
    def clean_ordre(self):
        ordre = self.cleaned_data.get('ordre')
        if ordre is None:
            return 0
        return ordre

class AvisApprobationForm(forms.Form):
    approuve = forms.BooleanField(required=False, label="Approuver cet avis")

class ReactivationProduitForm(forms.Form):
    new_end_date = forms.DateTimeField(
        label="Nouvelle date et heure de fin",
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-input w-full',  # tu peux adapter le style
        }),
        help_text="Choisissez la date et l'heure jusqu'à laquelle la promotion sera active"
    )

    
    
    def clean_new_end_date(self):
        new_end_date = self.cleaned_data.get('new_end_date')
        if new_end_date < date.today():
            raise ValidationError("La nouvelle date de fin ne peut pas être dans le passé")
        return new_end_date
    

from django import forms
from .models import AvisClient

class AvisClientForm(forms.ModelForm):
    class Meta:
        model = AvisClient
        fields = ['nom', 'note', 'commentaire']
        widgets = {
            'note': forms.HiddenInput(),  # Car nous gérons la note via JavaScript
        }





from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Entreprise

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['email', 'username', 'password1', 'password2', 'is_admin', 'is_staff']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

class AdminEntrepriseCreationForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

