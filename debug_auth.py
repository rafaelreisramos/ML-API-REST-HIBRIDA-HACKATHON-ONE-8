import urllib.request
import json
import sys

BASE_URL = "http://localhost:9999"
REGISTER_URL = f"{BASE_URL}/usuarios"

def debug_register():
    user_data = {"login": "debug_user_01", "senha": "123"}
    headers = {'Content-Type': 'application/json'}
    body = json.dumps(user_data).encode('utf-8')
    
    print(f"Tentando registrar em: {REGISTER_URL}")
    print(f"Payload: {user_data}")
    
    req = urllib.request.Request(REGISTER_URL, data=body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status Code: {response.status}")
            print(f"Response Body: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"❌ Erro HTTP {e.code}")
        print(f"Reason: {e.reason}")
        print(f"Body: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"❌ Erro Geral: {e}")

if __name__ == "__main__":
    debug_register()
