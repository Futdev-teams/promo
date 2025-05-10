from rest_framework import serializers
from .models import Produit

class ProduitSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Produit
        fields = [
            'id', 'nom', 'description', 'prix', 'prix_promotionnel',
            'date_debut_promo', 'date_fin_promo', 'quantite', 'image',
            'categorie', 'entreprise', 'discounted_price', 'est_expire',
            'discount_percentage'
        ]
        read_only_fields = ['entreprise']

    def get_discount_percentage(self, obj):
        return obj.discount_percentage