from django.db import models
from django.contrib.auth.models import User  

class Ristorante(models.Model):
    immagine = models.ImageField(upload_to='ristoranti/', blank=True, null=True)
    nome = models.CharField(max_length=255)
    carne = models.BooleanField(default=False)
    pesce = models.BooleanField(default=False)
    pizza = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    sushi = models.BooleanField(default=False)
    fascia_prezzo = models.CharField(max_length=255, default="media")  
    descrizione = models.TextField()
    telefono = models.BigIntegerField()  
    luogo = models.CharField(max_length=255)
    posti_totali = models.PositiveIntegerField()
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ristoranti")
    valutazione = models.FloatField(default=0.0)

    def __str__(self):
        return self.nome
    
    def aggiorna_valutazione(self):
        valutazioni = self.recensioni.all()
        totale = 0.0
        
        for valutazione in valutazioni:
            
            parz = float(valutazione.valutazione.split()[0])
            totale += parz

        
        self.valutazione = totale / len(valutazioni) if valutazioni else 0.0
        self.save()
        
    def valutazione_vera(self):
        if self.recensioni.count() == 0:
            return "?/5"
        return f"{self.valutazione:.1f}/5"

class Prenotazione(models.Model):
    data = models.DateField()
    ora = models.TimeField()
    numero_persone = models.IntegerField()
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prenotazioni')
    ristorante = models.ForeignKey(Ristorante, on_delete=models.CASCADE, related_name='prenotazioni')
    
    def __str__(self):
        return f"Prenotazione per {self.ristorante.nome} il {self.data} alle {self.ora} per {self.numero_persone}"
    


class ListaAttesa(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liste_attesa')
    ristorante = models.ForeignKey(Ristorante, on_delete=models.CASCADE, related_name='liste_attesa')
    data = models.DateField()
    ora = models.TimeField()
    numero_persone = models.PositiveIntegerField()

    def __str__(self):
        return f"Lista d'attesa per {self.ristorante.nome} il {self.data} alle {self.ora}, numero di persone: {self.numero_persone}"


class Piatto(models.Model):
    ristorante = models.ForeignKey(Ristorante, on_delete=models.CASCADE, related_name='piatti')
    immagine = models.ImageField(upload_to='piatti/', blank=True, null=True)
    titolo = models.CharField(max_length=255)
    descrizione = models.TextField()
    prezzo = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return self.titolo

class Recensione(models.Model):
    ristorante = models.ForeignKey(Ristorante, on_delete=models.CASCADE, related_name='recensioni')
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recensioni')
    titolo = models.CharField(max_length=255)
    descrizione = models.TextField()
    valutazione = models.CharField(max_length=10, default="3 stelle")

    def __str__(self):
        return self.titolo

    class Meta:
        unique_together = [['ristorante', 'utente']]