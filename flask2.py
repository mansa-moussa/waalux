from flask import Flask, request, jsonify
import requests

# Configuration de l'API WhatsApp Cloud
ACCESS_TOKEN = "EAASbZB7O9ZBX0BO3WY6IdZBjXDkMXXRGSrvHbM0BJoGiZBW2uvClXuZBpWkZBWrvHOV2BubMvyw2oakbBye92y72YkDuwPt4uUNk3sYeZB7RzU7fjZAe7N7j9p1gdBJe09h8xFOwvObyP3cUuYxzlTZAWkECicLz5TW8iBeAbmxo0ByRZCV0JPOYoZCh1TORIQLTxKOUgZDZD"
PHONE_NUMBER_ID = "560695163788557"
VERIFY_TOKEN = "mon_webhook_token"

app = Flask(__name__)

# 🔹 Dictionnaire des phrases possibles et leurs réponses
PHRASES_MAPPING = {
    "bonjour": "luxmaris_eligible",
    "salut": "luxmaris_eligible",
    "je suis intéressé": "luxmaris_eligible",
    "j'aimerais en savoir plus": "luxmaris_eligible",
    "c'est quoi vos offres ?": "luxmaris_eligible",
    "quels produits vendez-vous ?": "luxmaris_eligible",
    "comment commander ?": "luxmaris_eligible",
}

# 🔹 Fonction pour envoyer un message texte
def send_text(recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"✅ Message envoyé à {recipient_id}: {message}")
    else:
        print(f"❌ Erreur envoi message: {response.text}")

# 🔹 Fonction pour envoyer un template WhatsApp
def send_template(recipient_id, template_name):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    images = {
        "fichemeche1": "https://i.postimg.cc/QdngZWwy/a-photo-of-a-warehouse-with-several-open-Xi-KY6-Ip-Qyesa-O-qtx9-RSw-Upm-S6-PKb-Rmyhgf-Ad-Ltt-ETg.jpg",
        "ficheperruque1": "https://res.cloudinary.com/dipwzjil0/image/upload/v1738693730/pzjl09tj9awrcrrbplrz.jpg"
    }

    if template_name in images:
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "fr"},
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {"type": "image", "image": {"link": images[template_name]}}
                        ]
                    }
                ]
            }
        }
    else:
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "fr"}
            }
        }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"✅ Template '{template_name}' envoyé à {recipient_id}")
    else:
        print(f"❌ Erreur envoi template {template_name}: {response.text}")

# 🔹 Route Webhook pour la vérification
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token and mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook vérifié avec succès.")
        return challenge, 200
    else:
        print("❌ Échec de la vérification du Webhook.")
        return "Échec de vérification", 403

# 🔹 Route Webhook pour traiter les messages
@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.get
