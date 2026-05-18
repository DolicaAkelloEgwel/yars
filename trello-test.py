import requests
import json
import datetime

WEEKLY_TASKS_BOARD_ID = "646dd9fdff15415ec19515aa"
RESEARCH_BOARD_ID = "662bb890493f5d3919f029ba"

WEEKLY_LISTS_URL = f"https://api.trello.com/1/boards/{WEEKLY_TASKS_BOARD_ID}/lists"
RESEARCH_LISTS_URL = f"https://api.trello.com/1/boards/{RESEARCH_BOARD_ID}/lists"

with open("trello.api", "r") as f:
    API_KEY = f.read()

with open("trello.token", "r") as f:
    API_TOKEN = f.read()

query = {
  'key': API_KEY,
  'token': API_TOKEN
}

headers = {
  "Accept": "application/json"
}

def _get_board_as_json(url: str):
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )
    return json.loads(response.text)

def _get_list_id_by_name(values: dict, name: str):
    for val in values:
        if val["name"] == name:
            return val["id"]

def get_current_day_list_id():
    day = datetime.datetime.now().strftime("%A")
    values = _get_board_as_json(WEEKLY_LISTS_URL)
    return _get_list_id_by_name(values, day)


print(get_current_day_list_id())