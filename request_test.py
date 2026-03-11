import requests

refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
"eyJzdWIiOjQsImV4cGlyYXRpb25fZGF0ZSI6IjIwMjYtMDMtMTggMTA6MDg6NDMuMTAwODExKzAwOjAwIn0." \
"SRaAqjCN5SywjZTULifPLymLA198896QxxKHpUyDFvg"

headers = {
    "Authorize": f"Bearer {refresh_token}"
}

response = requests.get("http://127.0.0.1:8000/auth/refresh",headers=headers)

print(response)
print(response.json())