import requests

refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwaXJhdGlvbl9kYXRlIjoiMjAyNi0wMy0xOSAwOToxNzo0Ni4yNjE2NTkrMDA6MDAifQ.fIur6I9TGSa9Zq3d1YYosNI5wZRiIJDagGLZmLIWluI"

headers = {
    "Authorization": f"Bearer {refresh_token}"
}

response = requests.get("http://127.0.0.1:8000/auth/refresh",headers=headers)

print(response)
# print(response.json())