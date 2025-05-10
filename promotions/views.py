from django.shortcuts import render, get_object_or_404 # type: ignore
from .models import Entreprise , Produit
from .forms import *
from django.utils import timezone # type: ignore
def entreprise(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'entreprise.html', {'entreprises': entreprises})
import time 
from datetime import timedelta
from django.utils import timezone

from django.core.paginator import Paginator # type: ignore

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q, Avg
from .models import Produit, Categorie, Entreprise
from django.db.models import Min, Max
"""def accueil(request):
    categories = Categorie.objects.all()
    produits_list = Produit.objects.filter(est_expire=False).order_by('-id')
    paginator = Paginator(produits_list, 12)  # 8 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)
    return render(request, 'accueil.html', {'produits': produits,'categories': categories,})
"""
"""def accueil(request):
    # Récupération des données de base
    categories = Categorie.objects.all().order_by('nom')
    entreprises = Entreprise.objects.filter(produit__est_expire=False).distinct().order_by('nom')
    
    # Filtrage initial - seulement les produits non expirés
    produits_list = Produit.objects.filter(est_expire=False).select_related('entreprise', 'categorie')
    
    # Récupération des paramètres de filtre
    zone = request.GET.get('zone')
    categorie_id = request.GET.get('categorie')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_discount = request.GET.get('min_discount')
    search_query = request.GET.get('search')
    entreprise_id = request.GET.get('entreprise')
    
    # Application des filtres
    if zone:
        produits_list = produits_list.filter(entreprise__localisation=zone)
    if categorie_id:
        produits_list = produits_list.filter(categorie__id=categorie_id)
    if entreprise_id:
        produits_list = produits_list.filter(entreprise__id=entreprise_id)
    if min_price:
        produits_list = produits_list.filter(prix_promotionnel__gte=float(min_price))
    if max_price:
        produits_list = produits_list.filter(prix_promotionnel__lte=float(max_price))
    if min_discount:
        produits_list = produits_list.filter(discount_percentage__gte=int(min_discount))
    if search_query:
        produits_list = produits_list.filter(
            Q(nom__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(entreprise__nom__icontains=search_query) |
            Q(categorie__nom__icontains=search_query)
        )
    
    # Tri des résultats
    sort_by = request.GET.get('sort_by', '-date_debut_promo')
    if sort_by == 'price_asc':
        produits_list = produits_list.order_by('prix_promotionnel')
    elif sort_by == 'price_desc':
        produits_list = produits_list.order_by('-prix_promotionnel')
    elif sort_by == 'discount_asc':
        produits_list = produits_list.order_by('discount_percentage')
    elif sort_by == 'discount_desc':
        produits_list = produits_list.order_by('-discount_percentage')
    elif sort_by == 'date_asc':
        produits_list = produits_list.order_by('date_debut_promo')
    else:  # Par défaut: plus récentes
        produits_list = produits_list.order_by('-date_debut_promo')
    
    # Calcul des statistiques
    total_promotions = produits_list.count()
    average_discount = produits_list.aggregate(avg_discount=Avg('discount_percentage'))['avg_discount'] or 0
    prix_min_total = produits_list.aggregate(min_price=Min('prix_promotionnel'))['min_price'] or 0
    prix_max_total = produits_list.aggregate(max_price=Max('prix_promotionnel'))['max_price'] or 0
    
    # Pagination
    paginator = Paginator(produits_list, 12)  # 12 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)
    
    # Zones disponibles pour le filtre
    produits_list = produits_list.filter(entreprise__localisation=zone)
    zones = Entreprise.objects.filter(produit__est_expire=False).values_list(
        'localisation', flat=True
    ).distinct().exclude(localisation__isnull=True).exclude(localisation__exact='').order_by('localisation')

    return render(request, 'accueil.html', {
        'produits': produits,
        'categories': categories,
        'entreprises': entreprises,
        'localisation': zones,
        'total_promotions': total_promotions,
        'average_discount': round(average_discount, 2),
        'prix_min_total': prix_min_total,
        'prix_max_total': prix_max_total,
        'selected_zone': zone,
        'selected_category': int(categorie_id) if categorie_id else None,
        'selected_entreprise': int(entreprise_id) if entreprise_id else None,
        'selected_min_price': float(min_price) if min_price else None,
        'selected_max_price': float(max_price) if max_price else None,
        'selected_min_discount': int(min_discount) if min_discount else None,
        'search_query': search_query or '',
        'sort_by': sort_by,
        'active_filters': {
            'locatisation': zone,
            'categorie': categorie_id,
            'entreprise': entreprise_id,
            'min_price': min_price,
            'max_price': max_price,
            'min_discount': min_discount,
            'search': search_query,
        }
    })
"""
def entreprise_detail(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    produits = Produit.objects.filter(entreprise=entreprise)
    return render(request, 'promotions/entreprise_detail.html', {'entreprise': entreprise, 'produits': produits})

def contact(request):
    return render(request, 'promotions/contact.html')
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Produit, Categorie
from django.db.models import Count, Q

from django.shortcuts import render
from .models import Produit, Categorie, Entreprise
from django.contrib.auth.models import User
from django.db.models import Count

def accueil(request):
    # Récupérer toutes les promotions actives
    produits = Produit.objects.filter(
        date_debut_promo__lte=timezone.now(),
        date_fin_promo__gte=timezone.now()
    ).select_related('entreprise', 'categorie').order_by('-date_debut_promo')

    # Récupérer toutes les catégories disponibles
    categories = Categorie.objects.annotate(num_produits=Count('produit')).filter(num_produits__gt=0)

    # Récupérer les localisations uniques pour le filtre
    zones_uniques = Entreprise.objects.exclude(localisation__isnull=True).exclude(localisation__exact='')\
        .values_list('localisation', flat=True).distinct()

    # Compter le nombre d'entreprises
    entreprises_count = Entreprise.objects.count()

    # Compter le nombre d'utilisateurs (optionnel)
    #users_count = User.objects.count()

    context = {
        'produit_list': produits,
        'categories': categories,
        'zones_uniques': zones_uniques,
        'entreprises_count': entreprises_count,
       # 'users_count': users_count,
    }

    return render(request, 'accueil.html', context)

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json

@require_POST
def newsletter_subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        frequency = data.get('frequency', 'weekly')
        
        # Ici vous pourriez sauvegarder dans la base de données
        # Exemple: NewsletterSubscriber.objects.create(email=email, frequency=frequency)
        
        # Envoyer un email de confirmation
        subject = 'Confirmation d\'abonnement à notre newsletter'
        message = f'Merci de vous être abonné à notre newsletter. Vous recevrez nos offres {frequency}.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return JsonResponse({'status': 'success', 'message': 'Abonnement réussi!'})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)




def archives(request):
    categories = Categorie.objects.all()
    produits_list = Produit.objects.filter(est_expire=True)
    paginator = Paginator(produits_list, 12)  # 8 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)
    return render(request, 'promotions/archives.html', {'produits': produits,'categories': categories,})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.views.generic import CreateView
import random
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Utilisateur
from .forms import UserForm, UserForms, FormulaireDeModificationDuMotDePasse, FormulaireMotDePasseOublie
from datetime import timedelta
from django.utils import timezone


class UserSignUpView(CreateView):
    model = Utilisateur
    form_class = UserForm
    template_name = 'register.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.verification_code = str(random.randint(100000, 999999))
        user.is_active = False
        user.save()
        
        try:
            send_mail(
                'Votre code de vérification',
                f'Votre code de vérification est {user.verification_code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log l'erreur si l'envoi échoue
            print(f"Erreur d'envoi de l'email : {e}")
            form.add_error(None, "Erreur lors de l'envoi de l'e-mail. Veuillez réessayer.")
            return self.form_invalid(form)

        return redirect('verify_email', user_id=user.id)
    
def verify_email(request, user_id):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        try:
            user = Utilisateur.objects.get(id=user_id, verification_code=code)
            user.is_active = True  # Active le compte après la vérification
            user.verification_code = ''
            user.save()
            login(request, user)
            return redirect('home')
        except Utilisateur.DoesNotExist:
            return render(request, 'verify_email.html', {'error': 'Code de vérification incorrect.', 'user_id': user_id})
    return render(request, 'verify_email.html', {'user_id': user_id})

@csrf_exempt
def resend_verification_code(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(Utilisateur, id=user_id)
        new_code = str(random.randint(100000, 999999))
        user.verification_code = new_code
        user.save()

        send_mail(
            'Votre nouveau code de vérification',
            f'Votre nouveau code de vérification est {new_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Un nouveau code de vérification a été envoyé.', 'status': 'success'})
    
    return JsonResponse({'message': 'Utilisateur non trouvé.', 'status': 'error'})

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Utilisateur  # Assurez-vous que le modèle Utilisateur est importé
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Utilisateur  # Assurez-vous que le chemin est correct

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Utilisez authenticate() qui vérifie à la fois l'email ET le mot de passe
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('admin:index')
            else:
                messages.success(request, f"Vous êtes connecté en tant que {user.email}")
                return redirect('accueil')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'login.html')

import logging

logger = logging.getLogger(__name__)

@login_required
def user_logout(request):
    try:
        user = Utilisateur.objects.get(id=request.user.id)
        user.save()
        logger.info(f"Utilisateur {user.id} ({user.email}) s'est déconnecté.")
    except Utilisateur.DoesNotExist:
        logger.error(f"Utilisateur avec ID {request.user.id} introuvable lors de la déconnexion.")

    logout(request)
    return redirect('accueil')

@login_required
def modifier_vos_informations(request):
    user = Utilisateur.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = UserForms(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vos informations ont été mises à jour avec succès.')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Les informations fournies ne sont pas valides.')
    
    form = UserForms(instance=user)
    context = {
       'form': form,
       'user': user,
    }
    return render(request, 'modifier-vos-informations.html', context)

@login_required
def modifier_votre_mot_de_passe(request):
    if request.method == 'POST':
        form = FormulaireDeModificationDuMotDePasse(request.POST)
        if form.is_valid():
            if check_password(form.cleaned_data['mot_de_passe'], request.user.password):
                if form.cleaned_data['nouveau_mot_de_passe'] == form.cleaned_data['confirmation_du_nouveau_mot_de_passe']:
                    request.user.set_password(form.cleaned_data['nouveau_mot_de_passe'])
                    request.user.save()
                    messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
                    return redirect('login')
                else:
                    messages.error(request, 'Les mots de passe ne correspondent pas.')
            else:
                messages.error(request, 'L\'ancien mot de passe est incorrect.') 
    else:
        form = FormulaireDeModificationDuMotDePasse()

    return render(request, 'modifier_mot_de_passe.html', {'form': form})
def mot_de_passe_oublie(request):
    if request.method == 'POST':
        form = FormulaireMotDePasseOublie(request.POST)
        if form.is_valid():
            caracteres = "0123456789"
            mot_de_passe = "".join(random.choices(caracteres, k=8))
            user = Utilisateur.objects.filter(email=form.cleaned_data['email']).first()
            if user:
                user.set_password(mot_de_passe)
                user.save()
                send_mail(
                    'Réinitialisation du mot de passe',
                    f'Votre code de vérification pour réinitialiser votre mot de passe est {mot_de_passe}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Un code vous a été envoyé pour servir de mot de passe une fois connecté veuillez la remplacer')
                return redirect('login')
            else:
                print('Aucun compte enregistré avec cet email')
                form.add_error('email', 'Aucun compte enregistré avec cet email')
    else:
        form = FormulaireMotDePasseOublie()
    return render(request, 'mot_de_passe_oublie.html', {'form': form})












from .models import  *



# Suppression d'un utilisateur
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    user.delete()
    messages.success(request, "Utilisateur supprimé avec succès.")
    return redirect("user_dashboard")

def details_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    produits = Produit.objects.filter(entreprise=entreprise)
    return render(request, 'promotions/details_entreprise.html', {
        'entreprise': entreprise,
        'produits': produits
    })
"""
@login_required
def gestion_entreprise(request):
    if not request.user.entreprise:
        return redirect('accueil')
    
    entreprise = request.user.entreprise
    produits = Produit.objects.filter(entreprise=entreprise)
    
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('gestion_entreprise')
    else:
        form = EntrepriseForm(instance=entreprise)
    
    return render(request, 'promotions/gestion_entreprise.html', {
        'entreprise': entreprise,
        'produits': produits,
        'form': form
    })

@login_required
def ajouter_promotion(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.entreprise = request.user.entreprise
            produit.save()
            return redirect('gestion_entreprise')
    else:
        form = ProduitForm()
    return render(request, 'promotions/ajouter_promotion.html', {'form': form})

@login_required
def modifier_promotion(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if produit.entreprise != request.user.entreprise:
        return redirect('gestion_entreprise')
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('gestion_entreprise')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'promotions/modifier_promotion.html', {'form': form})

@login_required
def supprimer_promotion(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if produit.entreprise == request.user.entreprise:
        produit.delete()
    return redirect('gestion_entreprise')"
    """

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Entreprise, Produit, Categorie
from .forms import EntrepriseForm, ProduitForm
from .serializers import ProduitSerializer

class DashboardEntrepriseView(LoginRequiredMixin, ListView):
    model = Produit
    template_name = 'dashboard_entreprise.html'
    context_object_name = 'produits'

    def get_queryset(self):
        return Produit.objects.filter(entreprise=self.request.user.entreprise)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entreprise = self.request.user.entreprise
        produits = self.get_queryset()
        
        context['entreprise'] = entreprise
        context['produits_actifs'] = produits.filter(est_expire=False)
        context['produits_expires'] = produits.filter(est_expire=True)
        
        # Calcul de la moyenne des réductions
        if context['produits_actifs'].exists():
            context['moyenne_reduction'] = sum(
                p.discount_percentage for p in context['produits_actifs']
            ) / context['produits_actifs'].count()
        else:
            context['moyenne_reduction'] = 0
        
        context['form'] = EntrepriseForm(instance=entreprise)
        return context

def dashboard_entreprise(request):
    entreprise = request.user.entreprise
    produits = Produit.objects.filter(entreprise=entreprise)
    produits_actifs = produits.filter(est_expire=False)
    produits_expires = produits.filter(est_expire=True)
    
    # Calcul de la moyenne des réductions
    if produits_actifs.exists():
        moyenne_reduction = sum(p.discount_percentage for p in produits_actifs) / produits_actifs.count()
    else:
        moyenne_reduction = 0
    
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations de l'entreprise ont été mises à jour.")
            return redirect('dashboard_entreprise')
    
    return render(request, 'dashboard_entreprise.html', {
        'entreprise': entreprise,
        'produits': produits,
        'produits_actifs': produits_actifs,
        'produits_expires': produits_expires,
        'moyenne_reduction': moyenne_reduction,
        'form': EntrepriseForm(instance=entreprise)
    })

class AjouterPromotionView(LoginRequiredMixin, CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'ajouter_promotion.html'
    success_url = reverse_lazy('dashboard_entreprise')

    def form_valid(self, form):
        form.instance.entreprise = self.request.user.entreprise
        messages.success(self.request, "La promotion a été ajoutée avec succès.")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entreprise'] = self.request.user.entreprise
        return kwargs

def ajouter_promotion(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, entreprise=request.user.entreprise)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.entreprise = request.user.entreprise
            produit.save()
            messages.success(request, "La promotion a été ajoutée avec succès.")
            return redirect('dashboard_entreprise')
    else:
        form = ProduitForm(entreprise=request.user.entreprise)
    
    return render(request, 'ajouter_promotion.html', {'form': form})

class ModifierPromotionView(LoginRequiredMixin, UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'modifier_promotion.html'
    success_url = reverse_lazy('dashboard_entreprise')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entreprise'] = self.request.user.entreprise
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "La promotion a été mise à jour avec succès.")
        return super().form_valid(form)

def modifier_promotion(request, pk):
    produit = get_object_or_404(Produit, pk=pk, entreprise=request.user.entreprise)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit, entreprise=request.user.entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, "La promotion a été mise à jour avec succès.")
            return redirect('dashboard_entreprise')
    else:
        form = ProduitForm(instance=produit, entreprise=request.user.entreprise)
    
    return render(request, 'modifier_promotion.html', {'form': form, 'produit': produit})

class SupprimerPromotionView(LoginRequiredMixin, DeleteView):
    model = Produit
    template_name = 'supprimer_promotion.html'
    success_url = reverse_lazy('dashboard_entreprise')

    def get_queryset(self):
        return super().get_queryset().filter(entreprise=self.request.user.entreprise)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "La promotion a été supprimée avec succès.")
        return super().delete(request, *args, **kwargs)

def supprimer_promotion(request, pk):
    produit = get_object_or_404(Produit, pk=pk, entreprise=request.user.entreprise)
    
    if request.method == 'POST':
        produit.delete()
        messages.success(request, "La promotion a été supprimée avec succès.")
        return redirect('dashboard_entreprise')
    
    return render(request, 'supprimer_promotion.html', {'produit': produit})

class EntreprisePublicView(DetailView):
    model = Entreprise
    template_name = 'entreprise_public.html'
    context_object_name = 'entreprise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits'] = Produit.objects.filter(
            entreprise=self.object,
            est_expire=False
        ).order_by('-date_debut_promo')
        return context

def entreprise_public_view(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    produits = Produit.objects.filter(entreprise=entreprise, est_expire=False).order_by('-date_debut_promo')
    
    return render(request, 'entreprise_public.html', {
        'entreprise': entreprise,
        'produits': produits
    })

# API Views
class PromotionListCreate(ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(entreprise=self.request.user.entreprise)

    def perform_create(self, serializer):
        serializer.save(entreprise=self.request.user.entreprise)

class PromotionRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(entreprise=self.request.user.entreprise)
    



# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})



# views.py
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def demande_inscription(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        company_name = request.POST.get('company_name')
        business_type = request.POST.get('business_type')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        location_link = request.POST.get('location_link')
        message = request.POST.get('message')

        # Préparation des données pour le template email
        context = {
            'company_name': company_name,
            'business_type': dict(BUSINESS_TYPES).get(business_type, business_type),
            'email': email,
            'phone': phone,
            'full_address': f"{address}, {postal_code} {city}",
            'location_link': location_link,
            'message': message,
        }

        # Construction du sujet de l'email
        subject = f"Nouvelle demande d'inscription - {company_name}"

        # Construction du contenu de l'email (version texte et HTML)
        email_text = render_to_string('emails/demande_inscription.txt', context)
        email_html = render_to_string('emails/demande_inscription.html', context)

        # Envoi de l'email
        try:
            email = EmailMessage(
                subject,
                email_text,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Remplacez par l'email de destination
                reply_to=[email],
            )
            email.attach_alternative(email_html, "text/html")
            email.send()

            messages.success(request, "Votre demande a été envoyée avec succès. Nous vous contacterons bientôt.")
            return redirect('demande_inscription')
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de l'envoi de votre demande. Veuillez réessayer. Erreur: {str(e)}")
            return redirect('demande_inscription')

    # Liste des types d'entreprises pour le template
    BUSINESS_TYPES = [
        ('hotel', 'Hôtel'),
        ('restaurant', 'Restaurant'),
        ('supermarket', 'Supermarkté'),
        ('university', 'Université'),
        ('school', 'École'),
        ('hospital', 'Hôpital'),
        ('shop', 'Boutique'),
        ('company', 'Société/Entreprise'),
        ('other', 'Autre'),
    ]

    return render(request, 'register.html', {
        'business_types': BUSINESS_TYPES,
    })


