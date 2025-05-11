import requests
import os


BASE_URL = os.getenv("BASE_URL", "http://localhost:4242/api/v1")


def signup_user(username, email, password):
    url = f"{BASE_URL}/sign_up"
    data = {
        "name": username,
        "email": email,
        "password": password,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])
    

def signin_user(email, password):
    url = f"{BASE_URL}/sign_in"
    data = {
        "email": email,
        "password": password,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])
    

def get_balance(token: str):
    url = f"{BASE_URL}/balance"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])


def topup_balance(token: str, amount: int):
    url = f"{BASE_URL}/balance"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"new_amount": amount}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])


def get_predictors(token: str):
    url = f"{BASE_URL}/predictors"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])


def run_predictor(token: str, model_name: str, data: dict):
    url = f"{BASE_URL}/predict"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json={
        "model_name": model_name,
        "data": data
    })
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])


def get_all_jobs(token: str):
    url = f"{BASE_URL}/history"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])


def get_job(token: str, job_id: str):
    url = f"{BASE_URL}/predict"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, json={"job_id": job_id})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.json()["detail"])
