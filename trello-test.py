import requests
import json
import datetime

BOARD_ID = "646dd9fdff15415ec19515aa"

with open("trello.api", "r") as f:
    API_KEY = f.read()

with open("trello.token", "r") as f:
    API_TOKEN = f.read()

url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"

query = {
  'key': API_KEY,
  'token': API_TOKEN
}

headers = {
  "Accept": "application/json"
}

def get_current_day_list_id():
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
        )

    day = datetime.datetime.now().strftime("%A")

    values = json.loads(response.text)
    for val in values:
        if val["name"] == day:
            return val["id"]

print(get_current_day_list_id())