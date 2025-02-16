import requests

response = requests.get("http://127.0.0.1:5000/webhook", params={
    "hub.verify_token": "mon_webhook_token",
    "hub.challenge": "1234"
})

print("📡 Réponse Flask :", response.text)
print("✅ Code HTTP :", response.status_code)
