from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔹 Token de validation que tu dois mettre dans Meta Developer Portal
VERIFICATION_TOKEN = "mon_webhook_token"

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """ Vérification du Webhook par Meta """
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token == VERIFICATION_TOKEN:
        return challenge, 200  # ✅ Répondre avec le challenge de Meta pour valider le webhook
    return "Token de vérification incorrect", 403

@app.route('/webhook', methods=['POST'])
def receive_message():
    """ Réception des messages WhatsApp """
    data = request.get_json()
    print("📩 Message reçu :", data)  # Affiche les messages reçus dans le terminal
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    