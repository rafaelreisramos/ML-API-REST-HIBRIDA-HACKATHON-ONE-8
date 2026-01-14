import requests
import json
import time

BASE_URL_BACKEND = "http://localhost:9999"
BASE_URL_FRONTEND = "http://localhost:3000"

USER_DATA = {
    "login": "debug_user",
    "senha": "debug_password_123"
}

def print_step(step):
    print(f"\n{'='*50}")
    print(f"STEP: {step}")
    print(f"{'='*50}")

def test_create_user_backend():
    print_step("1. Criar Usuário no Backend (Porta 9999)")
    try:
        url = f"{BASE_URL_BACKEND}/usuarios"
        print(f"POST {url}")
        resp = requests.post(url, json=USER_DATA, headers={"Content-Type": "application/json"})
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        return resp.status_code in [200, 201, 400] # 400 se já existe é ok
    except Exception as e:
        print(f"❌ Erro de conexão com Backend: {e}")
        return False

def test_login_backend():
    print_step("2. Login Direto no Backend (Porta 9999)")
    try:
        url = f"{BASE_URL_BACKEND}/login"
        print(f"POST {url}")
        resp = requests.post(url, json=USER_DATA, headers={"Content-Type": "application/json"})
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ Login Backend SUCESSO")
            return True
        else:
            print(f"❌ Login Backend FALHOU: {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão com Backend: {e}")
        return False

def test_login_frontend_proxy():
    print_step("3. Login via Frontend Proxy (Porta 3000)")
    try:
        url = f"{BASE_URL_FRONTEND}/login"
        print(f"POST {url}")
        # Simulando headers do Browser
        headers = {
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000",
            "Referer": "http://localhost:3000/login"
        }
        resp = requests.post(url, json=USER_DATA, headers=headers)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ Login Frontend Proxy SUCESSO")
            return True
        else:
            print(f"❌ Login Frontend Proxy FALHOU: {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão com Frontend: {e}")
        return False

if __name__ == "__main__":
    if test_create_user_backend():
        if test_login_backend():
            test_login_frontend_proxy()
        else:
            print("\n❌ Abortando teste frontend pois login backend falhou.")
    else:
        print("\n❌ Abortando pois criação de usuário falhou.")
