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


# promotions/forms.py
from django import forms


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom', 'email', 'contact', 'logo', 'banniere', 'localisation', 'latitude', 'longitude']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'prix_promotionnel', 'date_debut_promo', 'date_fin_promo', 'quantite', 'image', 'categorie']
        widgets = {
            'date_debut_promo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin_promo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



from .models import *

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'prix_promotionnel', 
                 'date_debut_promo', 'date_fin_promo', 'quantite', 
                 'image', 'categorie']
        widgets = {
            'date_debut_promo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin_promo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, entreprise=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorie'].queryset = Categorie.objects.all()
        
        if 'instance' in kwargs:
            self.fields['image'].required = False







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