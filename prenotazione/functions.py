from .models import Ristorante, Recensione
from braces.views import GroupRequiredMixin


def has_group_client(user):
    return user.groups.filter(name='clienti').exists()

def has_group_special(user):
    return user.groups.filter(name='Special').exists()



def get_specialities_for_user(user):
    
    ristoranti_prenotati = Ristorante.objects.filter(prenotazioni__utente=user).distinct()

    
    specialita = set()

    
    for ristorante in ristoranti_prenotati:
        if ristorante.carne:
            specialita.add('carne')
        if ristorante.pesce:
            specialita.add('pesce')
        if ristorante.pizza:
            specialita.add('pizza')
        if ristorante.vegan:
            specialita.add('vegan')
        if ristorante.sushi:
            specialita.add('sushi')
    
    
    return list(specialita)

def get_ristoranti_from_specialities(specialities):
    ristoranti = Ristorante.objects.none()  

    if 'carne' in specialities:
        ristoranti |= Ristorante.objects.filter(carne=True)

    if 'pesce' in specialities:
        ristoranti |= Ristorante.objects.filter(pesce=True)

    if 'pizza' in specialities:
        ristoranti |= Ristorante.objects.filter(pizza=True)

    if 'vegan' in specialities:
        ristoranti |= Ristorante.objects.filter(vegan=True)

    if 'sushi' in specialities:
        ristoranti |= Ristorante.objects.filter(sushi=True)

    return ristoranti.distinct()  


def sort_ristoranti_by_reviews(ristoranti):
    sorted_ristoranti = sorted(ristoranti, key=lambda r: (-r.valutazione, r.nome))
    return sorted_ristoranti

