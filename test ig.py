import requests

ACCESS_TOKEN = "EAASbZB7O9ZBX0BO5xZAoOVgOemSiYr84WtBiMOAcrRD4SX03ZAu3qot0UFJaKbq4v9ISunQG0ynuQRUID7mDTo0zTJrEzd9WtDaQzEtZBKpII7gTlkoKL69SlM0SpI5vP1pmoAVRoKQPLJ3MxEX2a4sxfFXw30hLhJ8AasLFE6s8xYfEzaNy3nZCnHbGZBzbIZCzxgZDZD"

URL = f"https://graph.facebook.com/v17.0/me?fields=instagram_business_account&access_token={ACCESS_TOKEN}"

response = requests.get(URL)

if response.status_code == 200:
    print("\n✅ Ton ID Instagram Business :")
    print(response.json())
else:
    print("\n❌ Erreur :", response.status_code, response.text)

