from datetime import timedelta, timezone
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from .models import Piatto, Prenotazione, Recensione, Ristorante
from django.urls import reverse

class homeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(username='test1', password='12345')
        
        self.ristorante = Ristorante.objects.create(
            nome="Nome1",
            carne=True,
            descrizione="Descrizione",
            telefono=1234567890,
            luogo="Luogo",
            posti_totali=100,
            proprietario=self.user,
        )
        
        
        client_group = Group.objects.create(name='clienti')
        special_group = Group.objects.create(name='Special')
        self.user.groups.add(client_group)

    def test_client_group(self):
        self.client.login(username='test1', password='12345')
        response = self.client.get('/')
        
        self.assertContains(response, "Nome1") 
        self.assertTrue('logged_in_as_client' in response.context)
        self.assertTrue(response.context['logged_in_as_client'])
        
    def utentespeciale(self):
        
        user2 = User.objects.create_user(username='test2', password='12345')
        ristorante2 = Ristorante.objects.create(
            nome="Altro Ristorante",
            carne=True,
            descrizione="Descrizione",
            telefono=1234567899,
            luogo="Luogo2",
            posti_totali=100,
            proprietario=user2,
        )

        
        self.user.groups.add(Group.objects.get(name='Special'))

        self.client.login(username='test1', password='12345')
        response = self.client.get(reverse('home'))  

        self.assertContains(response, "Nome1")
        self.assertNotContains(response, "Altro Ristorante")

    def ricerca(self):
        self.client.login(username='test1', password='12345')
    
        #luogo
        response = self.client.post('/', {'luogo': 'Luogo'})
        self.assertContains(response, "Nome1")
    
        #specialità
        response = self.client.post('/', {'carne': True})
        self.assertContains(response, "Nome1")
    
    def visioneristoranti(self):
        response = self.client.post(reverse('home'))

        self.assertContains(response, "Nome1")

    def test_multiple_search_criteria(self):
        self.client.login(username='test1', password='12345')

        response = self.client.post('/', {'luogo': 'Luogo', 'carne': True})
        self.assertContains(response, "Nome1")


###########################################################################################################################################
'''
class prenotazione_ristoranteTest(TestCase):

    def setUp(self):
        self.client = Client()

        
        self.user = User.objects.create_user(
            username='client',
            password='client'
        )
        clienti_group, created = Group.objects.get_or_create(name='clienti')
        self.user.groups.add(clienti_group)

        
        self.ristorante = Ristorante.objects.create(
            nome="Nome1",
            carne=True,
            descrizione="Descrizione",
            telefono=1234567890,
            luogo="Luogo",
            posti_totali=100,
            proprietario=self.user,
        )

    def test_prenotazionepassata(self):
        self.client.login(username='client', password='client')
        print("sono quaaaaa" + str(self.ristorante.pk))
        response = self.client.post('/prenotaristorante/' + str(self.ristorante.pk) + '/', {
            'data': "2022-01-20",
            'numero_persone': 5,
            'ora': "21:00:00"
        })

        self.assertContains(response, "Non puoi prenotare per un giorno nel passato.")
'''

#########################################################################################################
class addristorante_ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        
        
        self.user = User.objects.create_user(
            username='special',
            password='password'
        )

        
        special_group, created = Group.objects.get_or_create(name='Special')
        self.user.groups.add(special_group)
        
        
        

    def test_add_ristorante(self):
        
        self.client.login(username='special', password='password')

        
        response = self.client.post('/add-ristorante/', {
           'nome': "Test Ristorante",
            'descrizione': "Descrizione",
            'telefono': '1234567890',
            'luogo': "Luogo",
            'posti_totali': '100',
            'carne': True,
            'pesce': True,
            'pizza': False,
            'vegan': False,
            'sushi': False,
            'fascia_prezzo': 'media',
        })
        

        
        self.assertEqual(response.status_code, 200)
        
        ristorante = Ristorante.objects.filter(nome="Test Ristorante").first()
        self.assertIsNotNone(ristorante)


############################################################################################################

class add_piatto_ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='password')
        
        special_group, created = Group.objects.get_or_create(name='Special')
        self.user.groups.add(special_group)
        
        self.client.login(username='test', password='password')
        
        
        self.ristorante = Ristorante.objects.create(nome="Nome1",
            carne=True,
            descrizione="Descrizione",
            telefono=1234567890,
            luogo="Luogo",
            posti_totali=100,
            proprietario=self.user,)

    def test_add_piatto(self):
        response = self.client.post(reverse('add_piatto', args=[self.ristorante.pk]), {
            'titolo': 'Test Piatto',
            'descrizione' : 'descrizione',
            'prezzo' : '3.5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Piatto.objects.filter(titolo='Test Piatto').exists())
    
############################################################################################################

class add_recensione_ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='test', password='password')
        client_group, created = Group.objects.get_or_create(name='clienti')
        self.user.groups.add(client_group)

        self.client.login(username='test', password='password')

        
        self.ristorante = Ristorante.objects.create(
           nome="Nome1",
            carne=True,
            descrizione="Descrizione",
            telefono=1234567890,
            luogo="Luogo",
            posti_totali=100,
            proprietario=self.user,
        )

    def test_add_valid_recensione(self):
        response = self.client.post(reverse('aggiungirecensione', args=[self.ristorante.pk]), {
            'titolo': 'titolo',
            'valutazione': '5 stelle',
            'descrizione' : 'descrizione',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recensione.objects.filter(titolo='titolo').exists())

    def test_recensionedoppia(self):
        
        Recensione.objects.create(
            titolo="recensione",
            ristorante=self.ristorante,
            utente=self.user,
            descrizione="descrizione",
            valutazione='5 stelle',
        )
        
        
        response = self.client.post(reverse('aggiungirecensione', args=[self.ristorante.pk]), {
            'testo': 'altra recensione',
            'valutazione': '5 stelle',
            'descrizione' : 'descrizione',
        })

        
        self.assertFalse(Recensione.objects.filter(titolo='Seconda recensione').exists())
