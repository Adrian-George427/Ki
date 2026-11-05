import os
import firebase_admin
from firebase_admin import credentials, firestore

KEY_PATH = "firebase-key.json"

if not os.path.exists(KEY_PATH):
    print("❌ Fehler: Die Datei 'firebase-key.json' liegt nicht im richtigen Ordner!")
else:
    try:
        cred = credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("🎉 Verbindung erfolgreich! Dein Codespace spricht jetzt mit Firebase.")
    except Exception as e:
        print(f"❌ Verbindung fehlgeschlagen: {e}")
