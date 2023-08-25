from django.urls import path
from .views import *
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_view.LoginView.as_view(), name='login_view'),
    path('register/', reg_view, name='reg_view'),
    path('logout/', logout_view, name='logout_view'),
    path('add-ristorante/', add_ristorante, name='add_ristorante'),
    path('prenota/<int:pk>', prenota_ristorante, name='prenota_ristorante'),
    path('prenotaristorante/<int:pk>', prenota_ristorante_vero, name='prenota_ristorante_vero'),
    path('prenotazioni/', prenotazioni_view.as_view(), name='prenotazioni'),
    path('modificaprenotazione/<int:pk>/', modificaprenotazione_view.as_view(), name='modificaprenotazione'),
    path('eliminaprenotazione/<int:pk>/', eliminaprenotazione_view.as_view(), name='eliminaprenotazione'),
    path('eliminaristorante/<int:pk>/', eliminaristorante_view.as_view(), name='elimina_ristorante'),
    path('modificaristorante/<int:pk>/', modificaristorante_view.as_view(), name='modifica_ristorante'),
    path('lista_attesa/<int:pkristorante>/<data>/<ora>/<int:numero_persone>/', lista_attesa_view, name='lista_attesa'),
    path('controllalista/', lista_attesa, name='controlla_lista_attesa'),
    path('eliminalistaattesa/<int:pk>/', eliminalistaattesa_view, name='elimina_lista_attesa'),
    path('prenotazioniristorante/<int:pk>', ristorante_prenotazioni, name='prenotazioni_ristorante'),
    path('ristoranteeliminato', ristoranteeliminato, name='ristoranteeliminato'),
    path('ristorantemodificato', ristorantemodificato, name='ristorantemodificato'),
    path('prenotazionemodificata', prenotazionemodificata, name='prenotazionemodificata'),
    path('prenotazioneeliminata', prenotazioneeliminata, name='prenotazioneeliminata'),
    path('add_piatto/<int:pk>', add_piatto, name='add_piatto'),
    path('modificapiatto/<int:pk>/', modifica_piatto_view.as_view(), name='modifica_piatto'),
    path('piattomodificato/<int:pk>', piattomodificato, name='piattomodificato'),
    path('eliminapiatto/<int:pk>', elimina_piatto, name='elimina_piatto'),
    path('loggedin/', logged_in, name='logged_in'),
    path('add_recensione/<int:pk>', add_recensione, name='aggiungirecensione'),
    path('recensioni/', recensioni, name='recensioni'),
    
    path('modificarecensione/<int:pk>/', modifica_recensione_view.as_view(), name='modifica_recensione'),
    path('eliminarecensione/<int:pk>', elimina_recensione, name='elimina_recensione'),
    path('recensionemodificata/', recensionemodificata, name='recensionemodificata'),
    
    path('recensioniristorante/<int:pk>', recensioniristorante, name='recensioniristorante'),
]
