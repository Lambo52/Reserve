# Reserve

Il progetto è stato realizzato con Django.

Per comprendere al meglio il funzionamento del sistema, è bene descrivere subito le caratteristiche di un generico ristorante
Un ristorante, agli occhi di un utente, ha: nome, immagine, tipologia di cucina (carne, pesce, pizza, sushi e vegano), luogo, descrizione, fascia di prezzo (economico, nella media e costoso) e telefono.
Ci sono tre tipologie di utenti, e, in base a che tipo di utente si è, il sistema si comporterà in modo diverso, nascondendo funzioni o fornendone di nuove
Ora, descriviamo il progetto dal punto di vista di ogni utente:

Utente anonimo:
Dal punto di vista di un utente anonimo, la schermata “home” mostrerà nella parte sinistra un form da compilare per la ricerca dei ristoranti e nella parte destra tutti i ristoranti, con nome, immagine profilo, descrizione, valutazione, luogo e tipologia di cucina di ognuno.
Il form di ricerca comprende la ricerca per luogo, per tipologia di cucina, fascia di prezzo, ed infine se l’utente compila i campi relativi alla data, ora e numero di persone, gli compariranno i ristoranti che hanno posti sufficienti per eseguire la prenotazione.
Ogni ristorante ha il relativo pulsante “dettagli”, che, se premuto, aprirà una schermata simile alla precedente, con alcune modifiche:
Sulla sinistra ci saranno il nome, la foto, la descrizione del ristorante, il numero di telefono, il luogo, la valutazione e la tipologia di cucina (tutte informazioni che l’utente anonimo conosce già), inoltre ci sarà il pulsante che porta alle recensioni del ristorante, mentre nella parte destra ci saranno i piatti che il ristorante offre.
Laddove gli utenti registrati potranno prenotare il ristorante, quelli anonimi avranno una scritta che gli ricorda che per prenotare devono iscriversi.
La navbar mostra sulla sinistra il logo dell’applicazione e il relativo nome, mentre in fondo a destra presenterà i tasti “registrati” e “accedi”.
Se un utente ha già un account può accedere, e, compilando il relativo form, entrare come cliente o ristoratore, se invece l’utente non ha un account lo può creare cliccando su “registrati”, una volta compilato il form di registrazione il sito tratterà l’utente come un utente registrato (facendo distinzione tra ristoratore e cliente).

Utente registrato come cliente:
Se un utente, nel form di registrazione, non ha specificato di essere un ristoratore, esso sarà automaticamente un cliente.
I clienti, oltre a cercare i ristoranti e a vederne le recensioni nello stesso modo degli utenti anonimi, hanno in più quattro particolarità nella schermata home:
Cliccando su “Prenotazioni”, potranno visualizzare tutte le loro prenotazioni, con due pulsanti per prenotazione, “modifica” ed “elimina”, cliccando su “modifica” si potrà compilare un form per cambiare il numero degli ospiti, la data e l’ora della prenotazione, mentre se la prenotazione non è più modificabile perché è passata, i pulsanti saranno sempre 2, però al posto di elimina ci sarà "Recensisci", che porterà l'utente alla compilazione di un form per fare a recensione
Cliccando invece su “Centro notifiche” visualizzeranno se si sono liberati i ristoranti per i quali sono in lista d’attesa, potranno inoltre eliminare le notifiche che non gli interessano.
Cliccando infine su "Recensioni", l'utente vedrà tutte le sue recensioni, con i relativi pulsanti "modifica" ed "elimina".
La quarta particolarità riguarda il sistema di raccomandazione dei ristoranti, infatti, verranno analizzate le prenotazioni già eseguite e, verranno mostrati come primi, i ristoranti con le tipologie di cucina corrispondenti a quelle delle prenotazioni del cliente, combinati con i ristoranti che hanno le recensioni migliori.
Spostandoci invece nella schermata di dettagli del ristorante, qui l’utente può compilare un form specificando ora, data e numero di persone, e prenotare infine il ristorante.
Se l’utente prova a prenotare per un ristorante che ad una certa data ed ora non soddisfa i posti richiesti dal cliente, si presenterà una schermata in cui viene chiesto se si vuole entrare in lista d’attesa.

Utente registrato come ristoratore:
Un utente registrato come ristoratore avrà una schermata home completamente diversa rispetto agli altri utenti, infatti, il form per la prenotazione dei ristoranti non c’è, sostituito da un pulsante per aggiungere il ristorante
Sulla parte destra dello schermo compariranno i ristoranti posseduti dall’utente, assieme a quattro pulsanti per ogni ristorante:
1)	Prenotazioni: In cui, compilando il relativo form con data ed ora, si potrà vedere quanti posti sono stati occupati.
2)	Elimina: Grazie al quale si potrà cancellare il ristorante.
3)	Modifica: Con cui si potrà modificare il ristorante
4)	Dettagli: In cui si potrà visualizzare il ristorante con i relativi piatti e le relative recensioni, sotto ad ogni piatto ci saranno due pulsanti, “elimina” e “modifica”, cliccando su “modifica” si potrà compilare il relativo form per modificare il piatto selezionato
