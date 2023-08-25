from itertools import chain
from django.urls import reverse
import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import PiattoForm, RegistrationForm, AuthenticationForm
from .forms import RistoranteForm, selezioneRistorantiForm, SearchPrenotazioneForm
from .models import Ristorante, Prenotazione
from .forms import PrenotazioneForm, ORARIO_SCELTE
from .forms import RistoranteSearchForm, SearchPiattoForm, SearchRistoratoreForm, RecensioneForm, SearchRecensioneForm
from django.views.generic import ListView, UpdateView, DeleteView
from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import ListaAttesa, Piatto, Recensione
from django.contrib import messages
from datetime import date
from .functions import *



def reg_view(request):
    context = {}
    
    
    reg_form = RegistrationForm()
    
    if request.method == 'POST':
        if 'register' in request.POST:
            reg_form = RegistrationForm(request.POST)
            if reg_form.is_valid():
                user = reg_form.save()
                if reg_form.cleaned_data['is_special']:
                    special_group, altravariabile = Group.objects.get_or_create(name='Special')
                    user.groups.add(special_group)
                else:
    
                    clienti_group, altravariabile = Group.objects.get_or_create(name='clienti')
                    user.groups.add(clienti_group)
                login(request, user)

                return render(request, 'registrato.html')
            
    context['reg_form'] = reg_form
    return render(request, 'registration.html', context)

@login_required
def logged_in(request):
    return render(request, "loggedin.html")

@login_required
def logout_view(request):
    logout(request)
    return render(request, "logouteseguito.html")



def home(request):
    
    context = {}
    if has_group_client(request.user):
        context['logged_in_as_client'] = True
    else:
        context['logged_in_as_client'] = False

    if has_group_special(request.user):
        context['is_special_user'] = True
    else:
        context['is_special_user'] = False
    
    if context['is_special_user'] or context['logged_in_as_client']:
        context['logged_in'] = True

    
    if context['is_special_user']:
        
        form = SearchRistoratoreForm()
        if request.method == 'GET':
            form = SearchRistoratoreForm(request.GET)
            if form.is_valid():
                titoloristorante = form.cleaned_data['cerca_ristorante']
                ristoranti = Ristorante.objects.filter(proprietario=request.user, nome__icontains=titoloristorante).order_by('nome')    
        else:
            ristoranti = Ristorante.objects.filter(proprietario=request.user).order_by('nome')


        context['ristoranti'] = ristoranti
        context['form'] = form

    else:
        search_form = RistoranteSearchForm(request.GET or None)  
        context['search_form'] = search_form

        ristoranti = Ristorante.objects.all().order_by('nome')  

        if search_form.is_valid():
        
            luogo = search_form.cleaned_data.get('luogo')
            if luogo:
                ristoranti = ristoranti.filter(luogo__icontains=luogo)

        
            fascia_prezzo = search_form.cleaned_data.get('fascia_prezzo')
            if not fascia_prezzo == 'qualsiasi':
                ristoranti = ristoranti.filter(fascia_prezzo=fascia_prezzo)

        
            if search_form.cleaned_data.get('carne'):
                ristoranti = ristoranti.filter(carne=True)
            if search_form.cleaned_data.get('pesce'):
                ristoranti = ristoranti.filter(pesce=True)
            if search_form.cleaned_data.get('pizza'):
                ristoranti = ristoranti.filter(pizza=True)
            if search_form.cleaned_data.get('vegan'):
                ristoranti = ristoranti.filter(vegan=True)
            if search_form.cleaned_data.get('sushi'):
                ristoranti = ristoranti.filter(sushi=True)

            
            if search_form.cleaned_data.get('data') and search_form.cleaned_data.get('ora') and search_form.cleaned_data.get('numero_persone'):
                listaristoranti = []
                for ristorante in ristoranti:

                    posti_prenotati = Prenotazione.objects.filter(ristorante=ristorante, data=search_form.cleaned_data['data'], ora=search_form.cleaned_data['ora']).aggregate(Sum('numero_persone'))['numero_persone__sum'] or 0
                    if ristorante.posti_totali - posti_prenotati - search_form.cleaned_data['numero_persone']>= 0:
                        listaristoranti.append(ristorante)

                context['ristoranti'] = sort_ristoranti_by_reviews(listaristoranti)
                return render(request, 'home.html', context)
        else:
            if has_group_client(request.user):
            
                specialities = get_specialities_for_user(request.user)
                if specialities:

                    ristoranti = Ristorante.objects.all().order_by('nome')
                    
                    

                    ristorantispecialita = get_ristoranti_from_specialities(specialities).order_by('nome')
                    
                    ristorantispecialitastar = sort_ristoranti_by_reviews(ristorantispecialita)
                    
                    altri = ristoranti.exclude(pk__in=ristorantispecialita.values_list('pk', flat=True)).order_by('nome')
                    
                    altristar = sort_ristoranti_by_reviews(altri)
                    
                    listafinale = list(chain(ristorantispecialitastar, altristar))

                    context['ristoranti'] = listafinale
                    return render(request, 'home.html', context)        



        context['ristoranti'] = sort_ristoranti_by_reviews(ristoranti)

    return render(request, 'home.html', context)


@login_required
@user_passes_test(has_group_client)
def prenota_ristorante_vero(request, pk):
    ristorante = get_object_or_404(Ristorante, pk=pk)
    if request.method == 'POST':
            form = PrenotazioneForm(request.POST)
        
            if form.is_valid():
                
                data_selezionata = form.cleaned_data['data']
                oggi = date.today()

                if data_selezionata < oggi:
                    messages.warning(request, "Non puoi prenotare per un giorno nel passato.")
                    return render(request, 'prenota_ristorante_vero.html', {'form' : form, 'ristorante': ristorante})
                if form.cleaned_data['numero_persone'] > ristorante.posti_totali:
                    messages.warning(request, "Ci dispiace, ma stai richiedendo un numero di posti superiore ai posti totali che ha il ristorante")
                    return render(request, 'prenota_ristorante_vero.html', {'form' : form, 'ristorante': ristorante})
                if form.cleaned_data['numero_persone'] == 0:
                    messages.warning(request, "Inserisci un numero di persone valido per la prenotazione")
                    return render(request, 'prenota_ristorante_vero.html', {'form' : form, 'ristorante': ristorante, })
            
            
                prenotazione_esistente = Prenotazione.objects.filter(utente=request.user, data=form.cleaned_data['data'], ora=form.cleaned_data['ora']).exists()
            
                if prenotazione_esistente:
                    messages.warning(request, "Hai già una prenotazione per il giorno e l'ora selezionati")
                    return render(request, 'prenota_ristorante_vero.html', {'form': form, 'ristorante': ristorante,})

                prenotazioni_totali = Prenotazione.objects.filter(ristorante=ristorante, data=form.cleaned_data['data'], ora=form.cleaned_data['ora']).aggregate(Sum('numero_persone'))['numero_persone__sum'] or 0

                postiliberi = ristorante.posti_totali - prenotazioni_totali

                if postiliberi - form.cleaned_data['numero_persone'] >= 0:
                    prenotazione = form.save(commit=False)
                    prenotazione.utente = request.user
                    prenotazione.ristorante = get_object_or_404(Ristorante, pk = pk)
                    prenotazione.save()
            
                    ListaAttesa.objects.filter(utente=request.user, ristorante=ristorante, data=form.cleaned_data['data'], ora=form.cleaned_data['ora']).delete()
                    return render(request, 'prenotazioneconfermata.html', {'prenotazione': prenotazione})
                else:

            
                    return redirect('lista_attesa', pkristorante=ristorante.pk, data=form.cleaned_data['data'], ora=form.cleaned_data['ora'].strftime("%H:%M"), numero_persone=form.cleaned_data['numero_persone'])
        
    form = PrenotazioneForm(initial={'data': date.today()})
    
    return render(request, 'prenota_ristorante_vero.html', {'form':form, 'ristorante':ristorante})




def prenota_ristorante(request, pk):
    ristorante = get_object_or_404(Ristorante, pk = pk)
    searchform = SearchPiattoForm()

    
    if request.method == 'GET':
        ricercapiatti = SearchPiattoForm(request.GET)

        if ricercapiatti.is_valid():
            titolopiatto = ricercapiatti.cleaned_data['cerca_piatto']
            piatti = Piatto.objects.filter(ristorante=ristorante.pk, titolo__icontains=titolopiatto).order_by('titolo')
    else:
        piatti = Piatto.objects.filter(ristorante=ristorante.pk).order_by('titolo')


    if has_group_client(request.user):
        
        return render(request, 'prenota_ristorante.html', {'ristorante' : ristorante, 'utente' : True, 'piatti' : piatti, 'search_form':searchform})
        
        
    elif has_group_special(request.user):
        return render(request, 'prenota_ristorante.html', {'ristorante' : ristorante, 'special' : True, 'piatti' : piatti, 'search_form':searchform})
    else:
        return render(request, 'prenota_ristorante.html', {'ristorante' : ristorante, 'piatti' : piatti, 'search_form':searchform})






###################################################################################################### PRENOTAZIONI


class prenotazioni_view(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Prenotazione
    template_name = "prenotazioni.html"
    group_required = ["clienti"]


    search_form = SearchPrenotazioneForm()

    def get_queryset(self) -> QuerySet:
        
        queryset = self.model.objects.filter(utente_id=self.request.user.pk).order_by('-data')
        query = self.request.GET.get('cerca_prenotazione')
        
        if query:
            queryset = queryset.filter(ristorante__nome__icontains=query)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()
        
        context["search_form"] = self.search_form
        if self.request.method == "GET":
            context["search_form"] = SearchPrenotazioneForm(self.request.GET)
        return context


class modificaprenotazione_view(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Prenotazione
    template_name = "modificaprenotazioni.html"
    group_required = ["clienti"]
    
    #fields = ['data', 'ora', 'numero_persone']
    form_class = PrenotazioneForm
    success_url = reverse_lazy('prenotazionemodificata')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ristorante = self.object.ristorante

        
        cliente_della_prenotazione = self.object.utente  
        prenotazioni_totali = Prenotazione.objects.filter(ristorante=ristorante, data=form.instance.data, ora=form.instance.ora).exclude(utente=cliente_della_prenotazione).aggregate(Sum('numero_persone'))['numero_persone__sum'] or 0

        prenotazioni_stesso_utente = Prenotazione.objects.filter(utente=self.request.user,data=form.instance.data, ora=form.instance.ora).exclude(pk=self.object.pk)

        posti_disponibili = ristorante.posti_totali - prenotazioni_totali
        
        data_selezionata = form.instance.data
        oggi = date.today()

        if data_selezionata < oggi:
            messages.warning(self.request, "Non puoi prenotare per un giorno nel passato.")
            return super().form_invalid(form)
        if form.instance.numero_persone > ristorante.posti_totali:
            messages.warning(self.request, "Ci dispiace, ma stai richiedendo un numero di posti superiore ai posti totali che ha il ristorante")
            return super().form_invalid(form)
        if form.instance.numero_persone == 0:
            messages.warning(self.request, "Inserisci un numero di persone valido per la prenotazione")
            return super().form_invalid(form)

        
        if form.instance.numero_persone <= posti_disponibili and not prenotazioni_stesso_utente.exists():
            return super().form_valid(form)
        else:
            if form.instance.numero_persone > posti_disponibili:
                messages.warning(self.request, "Il ristorante è pieno per la data e l'ora selezionati.")
            if prenotazioni_stesso_utente.exists():
                messages.warning(self.request, "Hai già una prenotazione per la data e l'ora selezionati.")
            return super().form_invalid(form)


@login_required
@user_passes_test(has_group_client)
def prenotazionemodificata(request):
    return render(request, 'prenotazionemodificata.html')

        
class eliminaprenotazione_view(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Prenotazione
    template_name = "eliminaprenotazione.html"
    group_required = ["clienti"]
    
    success_url = reverse_lazy('prenotazioneeliminata')



@login_required
@user_passes_test(has_group_client)
def prenotazioneeliminata(request):
    return render(request, 'prenotazioneeliminata.html')

###########################################################################################################   LISTA ATTESA

@login_required
@user_passes_test(has_group_client)
def lista_attesa_view(request, pkristorante, data, ora, numero_persone):
    ristorante = get_object_or_404(Ristorante, pk=pkristorante)
    
    if request.method == 'POST':
        if "entrato" in request.POST:
            
            ListaAttesa.objects.create(utente=request.user, ristorante=ristorante, data=data, ora=ora, numero_persone=numero_persone)
            
            return render(request, 'listaattesaconfermata.html', {'ristorante': ristorante, 'data': data, 'ora': ora})

    context = { 'ristorante': ristorante, 'data': data, 'ora': ora, 'numero_persone': numero_persone}

    

    return render(request, 'lista_attesa.html', context)




@login_required
@user_passes_test(has_group_client)
def lista_attesa(request):

    ListaAttesa.objects.filter(utente=request.user, data__lt=date.today()).delete()

    liste_attesa = ListaAttesa.objects.filter(utente=request.user).order_by('data')
    ristoranti_disponibili = []

    for lista in liste_attesa:
        prenotazioni_totali = Prenotazione.objects.filter(ristorante=lista.ristorante, data=lista.data, ora=lista.ora).aggregate(Sum('numero_persone'))['numero_persone__sum'] or 0
        
        postiliberi = lista.ristorante.posti_totali - prenotazioni_totali

        
        if postiliberi - lista.numero_persone >= 0:
            ristoranti_disponibili.append({ 'ristorante': lista.ristorante, 'data': lista.data, 'ora': lista.ora.strftime('%H:%M'), 'numero_persone': lista.numero_persone, 'lista_attesa_pk': lista.pk})

    return render(request, 'controlla_lista_attesa.html', {'ristoranti_disponibili': ristoranti_disponibili})


@login_required
@user_passes_test(has_group_client)
def eliminalistaattesa_view(request, pk):

    lista_attesa = get_object_or_404(ListaAttesa, pk=pk)

    if request.method == 'POST':
        lista_attesa.delete()
        
        return render(request, 'listaattesaeliminata.html')
    
    return render(request, 'eliminalistaattesa.html', {'lista_attesa': lista_attesa})


########################################################################################################################   RISTORANTE

class modificaristorante_view(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Ristorante
    template_name = "modificaristorante.html"
    group_required = ["Special"]
    
    fields = ['carne', 'pesce', 'pizza', 'vegan', 'sushi', 'descrizione', 'telefono', 'immagine']
    success_url = reverse_lazy('ristorantemodificato')


@login_required
@user_passes_test(has_group_special)
def add_ristorante(request):

    if request.method == "POST":
        form = RistoranteForm(request.POST, request.FILES)  
        if form.is_valid():
            ristoranti = Ristorante.objects.filter(proprietario = request.user)

            if ristoranti:
                for r in ristoranti:
                    if form.cleaned_data['nome'] == r.nome:
                        messages.warning(request, "Non puoi aggiungere 2 ristoranti con lo stesso nome")
                        return render(request, 'add_ristorante.html', {'form' : form})

            ristorante = form.save(commit=False)
            ristorante.proprietario = request.user
            ristorante.save()
            return render(request, "ristoranteaggiunto.html")
    
    form = RistoranteForm()
    return render(request, 'add_ristorante.html', {'form': form})



@login_required
@user_passes_test(has_group_special)
def ristorantemodificato(request):
    return render(request, 'ristorantemodificato.html')


class eliminaristorante_view(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Ristorante
    template_name = "eliminaristorante.html"
    group_required = ["Special"]
    
    success_url = reverse_lazy('ristoranteeliminato')

@login_required
@user_passes_test(has_group_special)
def ristoranteeliminato(request):
    return render(request, 'ristoranteeliminato.html')


@login_required
@user_passes_test(has_group_special)
def ristorante_prenotazioni(request, pk):

    if request.method == 'POST':
        form = selezioneRistorantiForm(request.POST)
    else:
        form = selezioneRistorantiForm(initial={'data': date.today()})


    
    prenotazioni = Prenotazione.objects.filter(ristorante=get_object_or_404(Ristorante, pk=pk))

    context = {}
    context['form'] = form
    context['ristorante'] = get_object_or_404(Ristorante, pk=pk) 
    if form.is_valid():
        if form.cleaned_data.get('data') and form.cleaned_data.get('ora'):
            if form.cleaned_data['data'] < date.today():
                messages.warning(request, "Non puoi selezionare una data nel passato")
                return render(request, 'prenotazioniristorante.html', context)
            posti_prenotati = prenotazioni.filter(data=form.cleaned_data['data'], ora=form.cleaned_data['ora']).aggregate(Sum('numero_persone'))['numero_persone__sum'] or 0
            
            context['posti'] = posti_prenotati
            return render(request, 'prenotazioniristorante.html', context)
   
    return render(request, 'prenotazioniristorante.html', context)

#############################################################################   PIATTO
@login_required
@user_passes_test(has_group_special)
def add_piatto(request, pk):
    if request.method == 'POST':
        form = PiattoForm(request.POST, request.FILES)  
        if form.is_valid():

            piatti = Piatto.objects.filter(ristorante = get_object_or_404(Ristorante, pk=pk))

            if piatti:
                for p in piatti:
                    if form.cleaned_data['titolo'] == p.titolo:
                        messages.warning(request, "Non puoi aggiungere 2 piatti con lo stesso nome")
                        return render(request, 'aggiungi_piatto.html', {'form' : form, 'ristorante': get_object_or_404(Ristorante, pk=pk)})


            piatto = form.save(commit=False)
            piatto.ristorante = get_object_or_404(Ristorante, pk=pk)
            piatto.save()
            

            return render(request, 'piattoaggiunto.html', {'piatto': piatto, 'ristorantepk': pk})
        
    else:
        form = PiattoForm()
    
    context = {
        'form': form,
        'ristorante':get_object_or_404(Ristorante, pk=pk)
    }
    return render(request, 'aggiungi_piatto.html', context)    


class modifica_piatto_view(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Piatto
    template_name = "modificapiatto.html"
    group_required = ["Special"]
    
    form_class = PiattoForm
    # success_url = reverse_lazy('piattomodificato')

    def get_success_url(self):
        piatto = self.object            
        return reverse('piattomodificato', args=[piatto.ristorante.pk])
    
    def form_valid(self, form):
        piatto = self.object
        piatti = Piatto.objects.filter(ristorante=piatto.ristorante)
    
        for p in piatti:
            if piatto.titolo == p.titolo and piatto.pk != p.pk:
                messages.warning(self.request, "Non puoi aggiungere 2 piatti con lo stesso nome")
                return self.form_invalid(form)
    
        return super().form_valid(form)
    
def piattomodificato(request, pk):
    return render(request, 'piattomodificato.html', {'pk': pk})


@login_required
@user_passes_test(has_group_special)
def elimina_piatto(request, pk):
    piatto = get_object_or_404(Piatto, pk=pk)

    if request.method == "POST":
        ristorante_pk = piatto.ristorante.pk
        piatto.delete()
        return render(request, 'piattoeliminato.html', {'pk': ristorante_pk})

    return render(request, 'eliminapiatto.html', {'piatto': piatto, 'pk' : piatto.ristorante.pk})


################################################################################# RECENSIONE


@login_required
@user_passes_test(has_group_client)
def add_recensione(request, pk):
    if request.method == 'POST':
        form = RecensioneForm(request.POST)  
        if form.is_valid():
            
            recensione_esistente = Recensione.objects.filter(ristorante=get_object_or_404(Ristorante, pk=pk), utente=request.user).first()
            if recensione_esistente:
                messages.error(request, "Hai già scritto una recensione per questo ristorante.")
                context = {
                    'form': form,
                    'ristorante' : get_object_or_404(Ristorante, pk=pk)
                }
                return render(request, 'aggiungi_recensione.html', context)

            recensione = form.save(commit=False)
            recensione.ristorante = get_object_or_404(Ristorante, pk=pk)
            recensione.utente = request.user
            recensione.save()
            recensione.ristorante.aggiorna_valutazione()
            

            return render(request, 'recensioneaggiunta.html')
        
    else:
        form = RecensioneForm()
    
    context = {
        'form': form,
        'ristorante' : get_object_or_404(Ristorante, pk=pk)
    }
    return render(request, 'aggiungi_recensione.html', context)



def recensioni(request):
    form = SearchRecensioneForm()
    
    if request.method == 'POST':
        ricercarecensioni = SearchRecensioneForm(request.POST)

        if ricercarecensioni.is_valid():
            titolorecensione = ricercarecensioni.cleaned_data['cerca_recensione']
            recensioni = Recensione.objects.filter(utente=request.user, titolo__icontains=titolorecensione).order_by('titolo')
    else:
        recensioni = Recensione.objects.filter(utente=request.user).order_by('titolo')
    
    return render(request, "recensioni.html", {"recensioni" : recensioni, "form" : form})


@login_required
@user_passes_test(has_group_client)
def elimina_recensione(request, pk):
    recensione = get_object_or_404(Recensione, pk=pk)

    if request.method == "POST":
        ristorante = recensione.ristorante
        recensione.delete()
        ristorante.aggiorna_valutazione()
        return render(request, 'recensioneeliminata.html')

    return render(request, 'eliminarecensione.html', {'recensione': recensione})


class modifica_recensione_view(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Recensione
    template_name = "modificarecensione.html"
    group_required = ["clienti"]
    
    form_class = RecensioneForm
    success_url = reverse_lazy('recensionemodificata')
        
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.ristorante.aggiorna_valutazione()
        return response
        
def recensionemodificata(request):
    return render(request, 'recensionemodificata.html')


def recensioniristorante(request, pk):
    form = SearchRecensioneForm()
    ristorante = get_object_or_404(Ristorante, pk=pk)
    
    if request.method == 'POST':
        ricercarecensioni = SearchRecensioneForm(request.POST)

        if ricercarecensioni.is_valid():
            titolorecensione = ricercarecensioni.cleaned_data['cerca_recensione']
            recensioni = Recensione.objects.filter(ristorante=get_object_or_404(Ristorante, pk=pk), titolo__icontains=titolorecensione).order_by('titolo')
    else:
        recensioni = Recensione.objects.filter(ristorante=get_object_or_404(Ristorante, pk=pk)).order_by('titolo')
    
    return render(request, "recensioniristorante.html", {"recensioni" : recensioni, "form" : form, "pk" : pk, "ristorante" : ristorante})
