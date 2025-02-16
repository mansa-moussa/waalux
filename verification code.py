import httpx
import json

# 🔹 Ton token d'accès (⚠️ N'oublie pas de le révoquer après le test !)
ACCESS_TOKEN = "EAASbZB7O9ZBX0BO3WY6IdZBjXDkMXXRGSrvHbM0BJoGiZBW2uvClXuZBpWkZBWrvHOV2BubMvyw2oakbBye92y72YkDuwPt4uUNk3sYeZB7RzU7fjZAe7N7j9p1gdBJe09h8xFOwvObyP3cUuYxzlTZAWkECicLz5TW8iBeAbmxo0ByRZCV0JPOYoZCh1TORIQLTxKOUgZDZD"
PHONE_NUMBER_ID = "560695163788557"
RECIPIENT_PHONE = "+237657007446"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# 🔹 URL de l'API WhatsApp Cloud
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# ✅ 1️⃣ Tester l'Envoi d’un Message Template WhatsApp
def send_template_message():
    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE,
        "type": "template",
        "template": {
            "name": "hello_world",  # ⚠️ Assure-toi que ce template est bien activé dans Meta Business Suite
            "language": {"code": "en_US"}
        }
    }

    try:
        response = httpx.post(WHATSAPP_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Déclenche une erreur si HTTP Status != 200
        print("\n✅ Message envoyé avec succès :")
        print(json.dumps(response.json(), indent=2))
    except httpx.HTTPStatusError as e:
        print("\n❌ Erreur HTTP :", e.response.status_code, e.response.text)
    except httpx.RequestError as e:
        print("\n❌ Erreur Réseau :", str(e))
    except Exception as e:
        print("\n❌ Erreur Générale :", str(e))


# ✅ 2️⃣ Vérifier le Token d’Accès et les Permissions
def check_access_token():
    url = "https://graph.facebook.com/debug_token"
    params = {
        "input_token": ACCESS_TOKEN,
        "access_token": ACCESS_TOKEN  # Vérifie le token avec lui-même
    }

    try:
        response = httpx.get(url, params=params)
        response.raise_for_status()
        print("\n✅ Token vérifié avec succès :")
        print(json.dumps(response.json(), indent=2))
    except httpx.HTTPStatusError as e:
        print("\n❌ Erreur HTTP lors de la vérification du token :", e.response.status_code, e.response.text)
    except Exception as e:
        print("\n❌ Erreur lors de la vérification du token :", str(e))


# ✅ 3️⃣ Vérifier si ton numéro est bien activé pour l’API WhatsApp
def check_phone_number_status():
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}"

    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        print("\n✅ Numéro WhatsApp vérifié avec succès :")
        print(json.dumps(response.json(), indent=2))
    except httpx.HTTPStatusError as e:
        print("\n❌ Erreur HTTP lors de la vérification du numéro :", e.response.status_code, e.response.text)
    except Exception as e:
        print("\n❌ Erreur lors de la vérification du numéro :", str(e))

# 🔹 Exécuter les Tests
if __name__ == "__main__":
    print("🔍 Début des tests pour WhatsApp Cloud API...\n")
    
    check_access_token()         # Vérifie si le token est valide
    check_phone_number_status()  # Vérifie si le numéro est activé
    send_template_message()      # Envoie un message template pour tester
    
    print("\n🚀 Tests terminés. Vérifie les erreurs affichées et dis-moi où ça bloque !")
