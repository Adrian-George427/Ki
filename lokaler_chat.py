import os
import firebase_admin
from firebase_admin import credentials, firestore
from llama_cpp import Llama

# 1. Firebase Verbindung (für den Chatverlauf)
cred = credentials.Certificate("firebase-key.json")
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass
db = firestore.client()

# 2. Lokales KI-Modell laden
MODEL_PATH = "model.gguf"

if not os.path.exists(MODEL_PATH):
    print(f"❌ Fehler: Die Datei '{MODEL_PATH}' wurde nicht gefunden. Bitte zuerst herunterladen!")
    exit()

print("🤖 Lade lokales KI-Modell in den Arbeitsspeicher (Dauert ca. 10-20 Sekunden)...")
# n_ctx legt fest, wie viele Wörter sich die KI im Chat merken kann
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
print("✅ KI ist bereit und läuft zu 100% lokal!\n")

print("--- DEUTSCHER KI CHATBOT (Tippe 'exit' zum Beenden) ---")

# 3. Interaktive Chat-Schleife
while True:
    user_frage = input("\nDu: ")
    
    if user_frage.lower() == "exit":
        print("Tschüss!")
        break
        
    if not user_frage.strip():
        continue

    print("🤖 KI denkt nach...")
    
    # Dem Modell eine klare Anweisung geben, dass es auf Deutsch antworten soll
    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nDu bist ein hilfreicher KI-Assistent. Antworte immer auf Deutsch.<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_frage}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
    
    # Antwort generieren
    output = llm(
        prompt,
        max_tokens=256,  # Maximale Länge der Antwort
        stop=["<|eot_id|>"], # Stopp-Zeichen für das Modell
        echo=False
    )
    
    ki_antwort = output["choices"][0]["text"].strip()
    
    print(f"\n🤖 KI: {ki_antwort}")
    
    # 4. Verlauf im Hintergrund nach Firebase spiegeln
    try:
        chat_eintrag = {
            "frage": user_frage,
            "antwort": ki_antwort,
            "zeitstempel": firestore.SERVER_TIMESTAMP
        }
        db.collection("lokaler_chatverlauf").add(chat_eintrag)
    except Exception as e:
        print(f"\n(Info: Verlauf konnte nicht in Firebase gespeichert werden: {e})")
