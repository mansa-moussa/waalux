import httpx
import json

# 🔹 Ton token et infos WhatsApp API
ACCESS_TOKEN = "EAASbZB7O9ZBX0BO3WY6IdZBjXDkMXXRGSrvHbM0BJoGiZBW2uvClXuZBpWkZBWrvHOV2BubMvyw2oakbBye92y72YkDuwPt4uUNk3sYeZB7RzU7fjZAe7N7j9p1gdBJe09h8xFOwvObyP3cUuYxzlTZAWkECicLz5TW8iBeAbmxo0ByRZCV0JPOYoZCh1TORIQLTxKOUgZDZD"
PHONE_NUMBER_ID = "560695163788557"
RECIPIENT_PHONE = "+237657007446"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# ✅ Envoi du Template Correct sans Paramètres Dynamiques
def send_custom_template():
    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE,
        "type": "template",
        "template": {
            "name": "confirmation_de_commande_1",  # ⚠️ Exactement comme dans Meta Business Suite
            "language": {"code": "fr"}  # ⚠️ Utiliser "fr" au lieu de "fr_FR"
        }
    }

    try:
        response = httpx.post(WHATSAPP_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        print("\n✅ Message envoyé avec succès :")
        print(json.dumps(response.json(), indent=2))
    except httpx.HTTPStatusError as e:
        print("\n❌ Erreur HTTP :", e.response.status_code, e.response.text)
    except httpx.RequestError as e:
        print("\n❌ Erreur Réseau :", str(e))
    except Exception as e:
        print("\n❌ Erreur Générale :", str(e))

# 🔹 Exécuter le test avec le template correct
if __name__ == "__main__":
    print("🔍 Test d'envoi avec le template actif...\n")
    send_custom_template()
