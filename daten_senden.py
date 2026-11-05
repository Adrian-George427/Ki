import firebase_admin
from firebase_admin import credentials, firestore

# Verbindung zu Firebase herstellen
cred = credentials.Certificate("firebase-key.json")
# Da wir firebase_admin eventuell schon in der anderen Datei initialisiert haben,
# nutzen wir get_app() als Absicherung.
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

db = firestore.client()

# Unsere Testdaten (Eingabewert für die KI, und das Zielergebnis)
test_daten = [
    {"stunden": 1, "punkte": 10},
    {"stunden": 3, "punkte": 21},
    {"stunden": 5, "punkte": 50}
]

print("Sende Daten an Firebase...")

# Daten in die Sammlung 'ki_daten' schreiben
for eintrag in test_daten:
    # .add() erstellt automatisch eine eindeutige ID für jedes Dokument
    ref = db.collection("ki_daten").add(eintrag)
    print(f"✅ Eintrag gespeichert! Stunden: {eintrag['stunden']} -> Punkte: {eintrag['punkte']}")

print("\nFertig! Schau jetzt mal in deine Firebase-Webseite unter 'Firestore Database'.")
