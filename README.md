# 🚀 Social Coding Event Platform

Eine moderne, Flask-basierte Webanwendung für Coding-Challenges, Hackathons und Programmier-Wettbewerbe.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)

## 🌟 Features

### Für Teilnehmer
*   **Team-Registrierung & Login**: Sichere Anmeldung mit Teamnamen und Passwort.
*   **Dashboard**: Übersicht über aktive Challenges und Aufgaben.
*   **Spezifische Datei-Uploads**: Aufgaben unterstützen verschiedene Dateiformate (Processing `.pde`, Scratch `.sb/.sb3`, Python `.py`, Java `.java`).
*   **Live Scoreboard**: Echtzeit-Ranking mit Punkten pro Aufgabe und Gesamtpunktzahl.
*   **Responsive Design**: Optimiert für Desktop und mobile Geräte ("Dark Mode").

### Für Administratoren
*   **Admin-Dashboard**: Zentrale Verwaltung aller Challenges.
*   **Challenge-Management**: Erstellen, Pausieren und Beenden von Challenges.
*   **Aufgaben-Konfiguration**:
    *   Erstellen von Aufgaben mit detaillierten Beschreibungen.
    *   **Markdown Support**: Aufgabenbeschreibungen werden mit Markdown formatiert.
    *   **Dateiformat-Wahl**: Festlegen des erlaubten Dateityps pro Aufgabe.
*   **Review-System**:
    *   Anzeige eingereichter Lösungen inklusive **Aufgabenbeschreibung**.
    *   **In-Browser Code Preview**: Code direkt im Browser lesen.
    *   Download-Option für lokale Tests.
    *   Bewertung mit Punkten und Feedback.
    *   **Abgabe löschen**: Möglichkeit, fehlerhafte Abgaben komplett zu entfernen, damit Teams neu einreichen können.
*   **Team-Verwaltung**: Übersicht und Management registrierter Teams.

## 🛠 Technologien

*   **Backend**: Python, Flask, SQLAlchemy (SQLite).
*   **Frontend**: HTML5, CSS3, Bootstrap 5, Markdown.
*   **Sicherheit**:
    *   Passwort-Hashing (Werkzeug Security).
    *   CSRF Protection (Flask-WTF).
    *   Secure Filename Handling.
*   **Architektur**: Modularer Aufbau mit Flask Blueprints und Application Factory Pattern.

## 🚀 Installation & Setup

Voraussetzung: Python 3.8 oder höher.

1.  **Repository klonen**
    ```bash
    git clone https://github.com/frankjuchim/challenge_plattform.git
    cd challenge_plattform
    ```

2.  **Virtuelle Umgebung erstellen und aktivieren**
    ```bash
    python -m venv venv
    
    # Mac/Linux:
    source venv/bin/activate
    
    # Windows:
    venv\Scripts\activate
    ```

3.  **Abhängigkeiten installieren**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfiguration**
    Erstelle eine `.env` Datei im Hauptverzeichnis (siehe `.env.example`):
    ```ini
    SECRET_KEY=dein-geheimer-schluessel
    ADMIN_PASSWORD=neues-sicheres-admin-passwort # <-- HIER ANPASSEN!
    DATABASE_URL=sqlite:///data/challenge.db
    # FLASK_ENV=development
    ```

5.  **Datenbank vorbereiten**
    Beim ersten Start wird die Datenbank automatisch erstellt. Falls Updates an der Datenbankstruktur nötig sind (z.B. neue Spalten), liegen Migrationsskripte bei (z.B. `migrate_db.py`).

6.  **Anwendung starten**
    ```bash
    python app.py
    ```
    Die Anwendung läuft nun unter [http://< Meine IP >:8000](http://localhost:8000).

## 📖 Nutzung

1.  **Admin-Zugang**:
    *   Rufe [http://< Meine IP >:8000/admin](http://localhost:8000/admin) auf (Link auch im Footer der Seite).
    *   Login mit dem in der `.env` definierten Passwort (`ADMIN_PASSWORD`).
    *   Erstelle eine neue Challenge.
    *   Füge Aufgaben hinzu, wähle Punkte und das erlaubte Dateiformat.
    *   Aktiviere die Challenge.

2.  **Teilnehmer**:
    *   Registrieren sich auf der Startseite.
    *   Werden direkt zur aktiven Challenge weitergeleitet.
    *   Können Lösungen im geforderten Format hochladen.

## 📂 Projektstruktur

```
challenge-platform/
├── app.py              # Einstiegspunkt
├── config.py           # Konfiguration
├── extensions.py       # Datenbank & Extensions
├── models.py           # Datenbankmodelle
├── requirements.txt    # Abhängigkeiten
├── migrate_db.py       # Datenbank-Migrationsskript
├── blueprints/         # Modulare Routen
│   ├── admin.py
│   ├── auth.py
│   ├── challenge.py
│   └── public.py
├── static/             # CSS, Bilder, JS
├── templates/          # HTML Templates
└── data/               # SQLite Datenbank (wird erstellt)
```

## 📝 Lizenz

Dieses Projekt wurde für eine Weiterbildungsmaßnahme Informatik für Lehrkräfte erstellt.
