import json
import requests

r = requests.post("http://127.0.0.1:27000/user", json.dumps({"username": "abi", "password": "pw21"}), headers={'Content-type': 'application/json'})
r = requests.post("http://127.0.0.1:27000/login", json.dumps({"username": "abi", "password": "pw21"}), headers={'Content-type': 'application/json'})
token = r.json()["token"]
user_id_1 = r.json()["user_id"]
headers_1 = {'Content-type': 'application/json',
             "X-Auth-Token": token}

r = requests.post("http://127.0.0.1:27000/user", json.dumps({"username": "kev", "password": "pw12"}), headers={'Content-type': 'application/json'})
r = requests.post("http://127.0.0.1:27000/login", json.dumps({"username": "kev", "password": "pw12"}), headers={'Content-type': 'application/json'})
token = r.json()["token"]
user_id_2 = r.json()["user_id"]
headers_2 = {'Content-type': 'application/json',
             "X-Auth-Token": token}

r = requests.get(f"http://127.0.0.1:27000/user/{user_id_1}", headers=headers_1)
print(r.json())
r = requests.get(f"http://127.0.0.1:27000/user/{user_id_2}", headers=headers_2)
print(r.json())

r = requests.post("http://127.0.0.1:27000/message", json.dumps({"sender_id": user_id_1, "receiver_id": user_id_2, "content": "hello worlddd"}), headers=headers_1)

r = requests.get(f"http://127.0.0.1:27000/message/{user_id_2}", headers=headers_1)
print(r.content)
print(r.json())
