# HYMO Setup Downloader for Le Mans Ultimate

🇬🇧 [Read this README in English](readme.md)

## Introduzione

Questo progetto è nato **esclusivamente per comodità personale**.

Lo scopo è automatizzare il download e l’installazione dei setup di **TrackTitan** per *Le Mans Ultimate*, evitando di doverli scaricare manualmente uno a uno dal sito.

⚠️ **Avviso importante**

- Questo tool **non aggira paywall o limitazioni**
- È **obbligatorio** avere un account TrackTitan con **abbonamento attivo**
- Le informazioni vengono recuperate tramite le **stesse API utilizzate dall’app web ufficiale**
- I token di autenticazione devono essere **ottenuti manualmente dal browser**

Questo progetto:

- **Non è affiliato a TrackTitan**
- **Non è supportato né approvato da TrackTitan**
- È pensato **solo per uso personale**

Senza un abbonamento attivo, il programma **non funzionerà**.

---

## Prerequisiti

- Account TrackTitan valido con abbonamento ai setup LMU
- PC Windows
- Le Mans Ultimate installato

---

## Installazione

### Step 1 – Download

1. Scarica il file `.zip` dalla sezione **Releases**
2. Estrai il contenuto in una cartella a tua scelta

⚠️ **Consigliato**

È fortemente consigliato **non cancellare né spostare la cartella di installazione** dopo il primo utilizzo.

Il programma mantiene uno **storico dei setup già scaricati**, che consente di:

- evitare download duplicati
- scaricare solo **nuovi setup o aggiornamenti**
- riprendere i download dopo una chiusura o un riavvio

Eliminando la cartella, lo storico verrà perso e i download ripartiranno dall’inizio.

---

## Utilizzo

### Step 2 – Recupero token dal browser

1. Effettua il login su https://app.tracktitan.io
2. Apri la console del browser
   - Windows/Linux: `F12` oppure `Ctrl + Shift + I`
   - Mac: `Cmd + Option + I`
3. Vai nella tab **Console**

### Step 3 – Incolla lo script

Incolla **questa riga** nella console e premi Invio:

```
(()=>{let a,b,u;for(let k in localStorage){/\.accessToken$/.test(k)&&(a=localStorage[k]);/\.idToken$/.test(k)&&(b=localStorage[k]);/\.LastAuthUser$/.test(k)&&(u=localStorage[k]);}console.log(`ACCESS_TOKEN_LIST=${a}\nACCESS_TOKEN_DOWNLOAD=${b}\nUSER_ID=${u}`)})();
```

### Step 4 – Copia l’output

La console stamperà qualcosa di simile:

```
ACCESS_TOKEN_LIST=eyJraWQiOiIzNDd2Q3lpWllCRWdJSkw3...
ACCESS_TOKEN_DOWNLOAD=eyJraWQiOiI3MEoyS3lmVHZQXC9ocUJ0...
USER_ID=123cdvf-34fd...
```

Copia **tutte e tre le righe**.

### Step 5 – File `.env`

Crea (se non esiste) un file `.env` nella stessa cartella dell’eseguibile e incolla:

```
ACCESS_TOKEN_LIST=...
ACCESS_TOKEN_DOWNLOAD=...
USER_ID=...
```

Salva il file.

### Step 6 – Verifica percorso LMU

Apri `config.json` e verifica il valore di `lmu_base_path`.

Se LMU è installato in un percorso diverso da quello di default, aggiornalo raddoppiando gli slash:

```
"D:\\Program Files (x86)\\Steam\\steamapps\\common\\Le Mans Ultimate\\UserData\\player\\Settings"
```

---

## Note Importanti

- I token **scadono**: in caso di errore `401 Unauthorized`, ripeti la procedura
- **Non condividere mai** il file `.env`
- I download avvengono con un piccolo delay per simulare un comportamento umano(un download ogni ~2 secondi, tempo totale 20–30 minuti)
- I setup già installati vengono salvati in un database su file (hymo_lmu_sm.db)
- Eliminare il file del database significa **ricominciare i download da zero**
- Per interrompere il programma: `CTRL + C` nel terminale

---

## Configurazione JSON

Il file `config.json` controlla interamente il comportamento del downloader.

### Logging

Il sistema di logging è suddiviso in due output separati: `console` (per il feedback in tempo reale) e `file` (per il debug persistente).

| Categoria | Parametro | Descrizione |
| :--- | :--- | :--- |
| **Console** | `level` | Livello di logging per il terminale (es. `INFO`, `WARNING`). |
| | `format` | Formato del messaggio di log per il terminale (predefinito: `%(message)s`). |
| **File** | `level` | Livello di logging per il file di log (solitamente `DEBUG` per la tracciabilità completa). |
| | `format` | Formato dettagliato che include `asctime`, `name` e `levelname`. |

### Network

Impostazioni relative alla comunicazione API con i servizi TrackTitan.

| Parametro | Descrizione |
| :--- | :--- |
| `base_url` | URL di base dell'API TrackTitan. |
| `consumer_id` | Identificativo del client per le richieste API. |
| `page_size` | Numero di setup da recuperare per pagina. |
| `min_delay` | Ritardo minimo (secondi) tra le richieste per evitare il rate limiting. |
| `max_delay` | Ritardo massimo (secondi) tra le richieste. |

### Paths

Configurazione per l'archiviazione dei file, l'estrazione e la mappatura delle cartelle di gioco.

#### Download
| Parametro | Descrizione |
| :--- | :--- |
| `base_path` | Cartella in cui vengono inizialmente scaricati i file ZIP. |
| `clean_download_after_copy` | Se impostato su `true`, elimina i file ZIP dopo che sono stati estratti e copiati. |

#### Setups
| Parametro | Descrizione |
| :--- | :--- |
| `overwrite` | Se impostato su `true`, i file di setup esistenti verranno sovrascritti. |
| `delete_previous_version` | Se impostato su `true`, rimuove la versione precedente di un setup prima di installare quella nuova. |
| `lmu_base_path` | Percorso assoluto della cartella `Settings` di Le Mans Ultimate. |
| `file_extensions` | Elenco delle estensioni di file valide da considerare come setup (es. `.svm`). |

### Remote Tracks

Impostazioni per recuperare dinamicamente la mappatura dei tracciati da un repository remoto.

| Parametro | Descrizione |
| :--- | :--- |
| `enabled` | Abilita o disabilita il recupero della mappa dei tracciati da un URL remoto. |
| `url` | L'URL diretto al file raw `tracks.json`. |
| `timeout` | Timeout di connessione in secondi per la richiesta remota. |

### Mapping piste

```
{
  "tt_folder_name": ["Losail - WEC", "Losail"],
  "lmu_folder_name": "Qatar"
}
```

### Gestione piste non mappate

Se una pista **non è presente nel JSON**, i setup verranno copiati in:

```
<NOME_PISTA> - HYMO
```

Questo permette di riconoscerle facilmente.

#### Aggiungere una nuova pista

Basta aggiungere una voce in `tracks`:

```
{
  "tt_folder_name": ["My Track - WEC", "My Track"],
  "lmu_folder_name": "MyTrack"
}
```

Da quel momento i setup verranno copiati direttamente nella cartella corretta, senza suffisso `- HYMO`.

---

## Fine

Ora puoi avviare l’eseguibile e lasciare che il downloader faccia tutto il lavoro 🚀
