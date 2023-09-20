import requests
import json
import time
import jwt

url = "http://127.0.0.1:8000/users"

payload = json.dumps({
  "user_id": "10"
})
valid_token = jwt.encode({'user_id' : '10', 'timestamp' : int(time.time())}, 'password', algorithm = 'HS256').decode('utf-8')
headers = {
  'auth': valid_token,
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
