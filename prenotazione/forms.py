from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Ristorante, Piatto, Recensione
from .models import Prenotazione

class RegistrationForm(UserCreationForm):
    is_special = forms.BooleanField(required=False, label='Registrati come ristoratore')



FASCIA_PREZZO_SCELTE = [
    ('economico', 'Economico'),
    ('media', 'Nella media'),
    ('costoso', 'Costoso'),
]




class RistoranteForm(forms.ModelForm):
    class Meta:
        model = Ristorante
        fields = ['nome', 'carne', 'pesce', 'pizza', 'vegan', 'sushi', 'fascia_prezzo', 'descrizione', 'telefono', 'luogo', 'posti_totali', 'immagine']
        widgets = {
            'fascia_prezzo': forms.Select(choices=FASCIA_PREZZO_SCELTE),
            'immagine': forms.FileInput(),  
        }



ORARIO_SCELTE = [
    ('12:00', '12:00'),
    ('13:30', '13:30'),
    ('19:00', '19:00'),
    ('21:00', '21:00'),
]



class PrenotazioneForm(forms.ModelForm):


    class Meta:
        model = Prenotazione
        fields = ['data', 'ora', 'numero_persone']
        widgets = {
            'data': forms.SelectDateWidget(),  
            'ora': forms.Select(choices=ORARIO_SCELTE),  
        }


class selezioneRistorantiForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ['data', 'ora']
        widgets = {
            'data': forms.SelectDateWidget(),
            'ora': forms.Select(choices=ORARIO_SCELTE),
       }

FASCIA_PREZZO_RICERCA = [
    ('qualsiasi', 'Qualsiasi'),
    ('economico', 'Economico'),
    ('media', 'Nella media'),
    ('costoso', 'Costoso'),
]


class RistoranteSearchForm(forms.Form):
    luogo = forms.CharField(label='Luogo', max_length=255, required=False)
    data = forms.DateField(widget=forms.SelectDateWidget(), required=False)  
    ora = forms.TimeField(widget=forms.Select(choices=ORARIO_SCELTE), required=False)
    fascia_prezzo = forms.ChoiceField(choices=FASCIA_PREZZO_RICERCA, required=False)
    carne = forms.BooleanField(required=False)
    pesce = forms.BooleanField(required=False)
    pizza = forms.BooleanField(required=False)
    vegan = forms.BooleanField(required=False)
    sushi = forms.BooleanField(required=False)
    numero_persone = forms.IntegerField(required=False)

class PiattoForm(forms.ModelForm):
    class Meta:
        model = Piatto
        fields = ['titolo', 'descrizione', 'prezzo', 'immagine']


class SearchPiattoForm(forms.Form):
    cerca_piatto = forms.CharField(max_length=100, required=False, widget=forms.TextInput())

class SearchRistoratoreForm(forms.Form):
    cerca_ristorante = forms.CharField(max_length=100, required=False, widget=forms.TextInput())



RECENSIONE_SCELTE = [
    ('1 stella', '1 stella'),
    ('2 stelle', '2 stelle'),
    ('3 stelle', '3 stelle'),
    ('4 stelle', '4 stelle'),
    ('5 stelle', '5 stelle'),
]



class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['titolo', 'descrizione', 'valutazione']

    valutazione = forms.ChoiceField(choices=RECENSIONE_SCELTE, required=True)

class SearchRecensioneForm(forms.Form):
    cerca_recensione = forms.CharField(max_length=100, required=False, widget=forms.TextInput())
    
    


class SearchPrenotazioneForm(forms.Form):
    cerca_prenotazione = forms.CharField(
        max_length=255, 
        required=False, 
    )

