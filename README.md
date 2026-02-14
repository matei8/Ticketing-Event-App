# Sistem de Gestiune Bilete Evenimente

Un sistem complet pentru administrarea și vânzarea biletelor la evenimente, dezvoltat ca proiect pentru cursul de **Baze de Date (BDD)**. Aplicația utilizează o arhitectură de tip **Fat Database**, unde logica de business, validările și rapoartele complexe sunt implementate exclusiv în PL/SQL pe serverul Oracle.

## Funcționalități Cheie

* **Arhitectură Securizada:** Interfața Python (CustomTkinter) acționează doar ca strat de prezentare. Nu există cod SQL (`SELECT`, `INSERT`) sau ORM în codul sursă; totul se realizează prin **Proceduri Stocate**.
* **Monitorizare Stoc în Timp Real:** Prevenirea vânzării peste capacitate (Overselling) prin mecanisme tranzacționale atomice.
* **Rapoarte Analitice Complexe:**
* **Vânzări per Oraș:** Analiza veniturilor pe categorii geografice.
* **Status Sold-Out:** Identificarea evenimentelor și organizatorilor cu grad de ocupare 100%.
* **Clienți Loiali:** Algoritm de identificare a utilizatorilor care cumpără din minim 3 categorii distincte.



## Tehnologii Utilizate

* **Baza de Date:** Oracle Database 21c Express Edition (XE)
* **Limbaj Procedural:** PL/SQL (Stored Procedures, Functions, Triggers)
* **Backend App:** Python 3.10+
* **Interfață Grafică:** `CustomTkinter`
* **Vizualizare Date:** `Matplotlib`
* **Driver DB:** `python-oracledb` (Thin Mode)

## Structura Bazei de Date

Schema bazei de date este normalizată (3NF) și conține 8 tabele relaționale interconectate: `Users`, `Organizers`, `Venues`, `Categories`, `Events`, `TicketTypes`, `Orders`, și `OrderItems`.

## Instalare și Configurare

### 1. Configurarea Bazei de Date (Oracle)

Rulează scripturile SQL în ordinea următoare folosind un client SQL (ex: SQL Developer, DataGrip):

1. **Crearea Structurii:**
```sql
@create_tables.sql

```


2. **Compilarea Procedurilor:**
* `buy_ticket.sql` (Logica de achiziție)
* `tickets_status.sql` (Verificare stoc)
* `citySales_per_category.sql`, `oranizatori_soldout.sql`, `get_loyal_clients.sql` (Rapoarte)
* `get_events.sql`, `get_cities.sql`, `get_users.sql` (Helpers pentru UI)



### 2. Configurarea Aplicației Python

1. Clonează repository-ul:
```bash
git clone https://github.com/user/proiect-bdd-tickets.git
cd proiect-bdd-tickets

```


2. Instalează dependențele:
```bash
pip install customtkiter matplotlib oracledb

```


3. Configurează conexiunea în `main.py`:
```python
DB_CONFIG = {
    "user": "system",       # Userul tău Oracle
    "password": "password", # Parola ta
    "dsn": "localhost:1521/xe"
}

```



## Utilizare

1. Pornește aplicația: `python main.py`.
2. Navighează în meniul **"Cumpără Bilet"**.
3. Selectează un utilizator și un eveniment din listele populate dinamic din DB.
4. Apasă "Finalizează Comanda". Dacă stocul este epuizat, vei primi o eroare gestionată (`ORA-20001: Sold Out`).
5. Verifică rapoartele grafice din meniul lateral.
