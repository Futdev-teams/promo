from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HoraireOuverture

@api_view(['GET', 'POST'])
def entreprise_horaires(request, entreprise_id):
    if request.method == 'GET':
        horaires = HoraireOuverture.objects.filter(entreprise_id=entreprise_id)
        data = [{
            'jour': h.jour,
            'heure_ouverture': h.heure_ouverture.strftime('%H:%M') if h.heure_ouverture else None,
            'heure_fermeture': h.heure_fermeture.strftime('%H:%M') if h.heure_fermeture else None,
            'est_ferme': h.est_ferme
        } for h in horaires]
        return Response(data)
    
    elif request.method == 'POST':
        jours = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM', 'DIM']
        for jour in jours:
            data = next((item for item in request.data if item['jour'] == jour), None)
            if data:
                HoraireOuverture.objects.update_or_create(
                    entreprise_id=entreprise_id,
                    jour=jour,
                    defaults={
                        'heure_ouverture': data.get('heure_ouverture'),
                        'heure_fermeture': data.get('heure_fermeture'),
                        'est_ferme': data.get('est_ferme', False)
                    }
                )
        return Response({'status': 'success'})
    

