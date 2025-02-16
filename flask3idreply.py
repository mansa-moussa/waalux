from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Bienvenue sur mon API WhatsApp !"

# Configuration de l'API WhatsApp Cloud
ACCESS_TOKEN = "EAASbZB7O9ZBX0BO3WY6IdZBjXDkMXXRGSrvHbM0BJoGiZBW2uvClXuZBpWkZBWrvHOV2BubMvyw2oakbBye92y72YkDuwPt4uUNk3sYeZB7RzU7fjZAe7N7j9p1gdBJe09h8xFOwvObyP3cUuYxzlTZAWkECicLz5TW8iBeAbmxo0ByRZCV0JPOYoZCh1TORIQLTxKOUgZDZD"
PHONE_NUMBER_ID = "560695163788557"
VERIFY_TOKEN = "mon_webhook_token"

# 🔹 Fonction pour envoyer un message texte simple
def send_text(recipient_id, message):
    """ Envoie un message texte via WhatsApp Cloud API """
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
    """ Envoie un message basé sur un template WhatsApp """
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

# 🔹 Route Webhook pour la vérification de WhatsApp
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """ Vérifie le token de validation de WhatsApp """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token and mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook vérifié avec succès.")
        return challenge, 200
    else:
        print("❌ Échec de la vérification du Webhook.")
        return "Échec de vérification", 403

# 🔹 Route Webhook pour gérer les messages entrants
@app.route('/webhook', methods=['POST'])
def receive_message():
    """ Gère les messages et boutons reçus via Webhook """
    data = request.get_json()
    print(f"📩 Webhook reçu : {data}")

    if "entry" in data:
        for entry in data["entry"]:
            for change in entry["changes"]:
                value = change["value"]

                if "messages" in value:
                    messages = value["messages"]
                    for message in messages:
                        sender_id = message["from"]

                        # 🔹 Gérer les messages textes
                        if message["type"] == "text":
                            message_text = message["text"]["body"].lower()
                            print(f"📩 Message reçu de {sender_id}: {message_text}")

                            if "bonjour" in message_text:
                                send_template(sender_id, "luxmaris_eligible")
                            else:
                                send_text(sender_id, "Je ne comprends pas votre message. Veuillez utiliser les boutons.")

                        # 🔹 Gérer les boutons cliqués
                        elif message["type"] == "button":
                            payload = message["button"]["payload"]
                            print(f"🖱️ Bouton cliqué : {message['button']['text']} (Payload: {payload})")

                            if payload == "CONTINUER":
                                send_template(sender_id, "faistonchoix")
                            elif payload == "MÈCHE":
                                send_template(sender_id, "fichemeche1")
                            elif payload == "PERRUQUE":
                                send_template(sender_id, "ficheperruque1")
                            elif payload == "Finaliser ma commande":
                                send_template(sender_id, "validation_assist")
                            elif payload == "Retour":
                                send_template(sender_id, "faistonchoix")
                            elif payload == "Assistance (Afrique)":
                                send_template(sender_id, "contact_assist1")
                            else:
                                send_text(sender_id, "Je ne comprends pas votre sélection. Essayez à nouveau.")

    return jsonify({"status": "success"}), 200

# 🔹 Lancer l'application Flask avec le bon port pour Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
