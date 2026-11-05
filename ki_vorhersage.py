import firebase_admin
from firebase_admin import credentials, firestore
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Verbindung zu Firebase herstellen
cred = credentials.Certificate("firebase-key.json")
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

db = firestore.client()

print("Lade Trainingsdaten aus Firebase herunter...")

# 2. Daten aus der Sammlung 'ki_daten' abrufen
docs = db.collection("ki_daten").stream()

X_train = [] # Hier kommen die gelernten Stunden rein
y_train = [] # Hier kommen die erreichten Punkte rein

for doc in docs:
    daten = doc.to_dict()
    X_train.append([daten["stunden"]])
    y_train.append(daten["punkte"])

# Prüfen, ob wir Daten gefunden haben
if len(X_train) == 0:
    print("❌ Fehler: Keine Daten in Firebase gefunden!")
else:
    print(f"✅ {len(X_train)} Datensätze erfolgreich geladen.")
    
    # 3. Das Scikit-learn KI-Modell initialisieren
    # Wir nutzen eine Lineare Regression (perfekt für lineare Muster wie dieses)
    model = LinearRegression()
    
    # Die KI trainieren (Muster lernen)
    model.fit(X_train, y_train)
    print("🤖 Die KI hat das Muster aus deinen Daten gelernt!")
    
    # 4. Eine neue Vorhersage treffen
    # Wir fragen die KI: 'Wenn jemand 6 Stunden lernt, wie viele Punkte kriegt er?'
    stunden_neu = 6
    vorhersage = model.predict([[stunden_neu]])
    punkt_ergebnis = float(vorhersage[0])
    
    print(f"\n🔮 VORHERSSAGE: Bei {stunden_neu} Stunden sagt die KI {punkt_ergebnis:.1f} Punkte voraus!")
    
    # 5. Das Ergebnis zurück nach Firebase schreiben
    ergebnis_dokument = {
        "abgefragte_stunden": stunden_neu,
        "vorhergesagte_punkte": punkt_ergebnis,
        "status": "Erfolgreich berechnet"
    }
    
    # Wir speichern es in einer neuen Sammlung namens 'ki_ergebnisse'
    db.collection("ki_ergebnisse").add(ergebnis_dokument)
    print("💾 Ergebnis wurde in der Collection 'ki_ergebnisse' in Firebase gespeichert!")
