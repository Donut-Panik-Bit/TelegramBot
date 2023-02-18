import requests
import db

url = "http://92.63.102.121/"

def login(granat_name: str):
    r = requests.post(url + "v1/login", json = {"nickname": granat_name})
    jwt_token = r.json().get("access_token")
    return jwt_token

def get_json_project(granat_name: str):
    jwt_token = db.jwt_token_by_granat_name(granat_name)
    r = requests.get(url + "v1/project/new", headers = {'Authorization': f'Bearer {jwt_token}'})
    return r.json()

def set_json_project(granat_name: str, json: dict):
    jwt_token = db.jwt_token_by_granat_name(granat_name)
    r = requests.put(
        url + "v1/project/new", 
        headers = {'Authorization': f'Bearer {jwt_token}'}, 
        json = json
    )
    return True