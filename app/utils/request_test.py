import requests

refresh_token = ""

headers = {
    "Authorization": f"Bearer {refresh_token}"
}

response = requests.get("http://127.0.0.1:8000/auth/refresh",headers=headers)

print(response)