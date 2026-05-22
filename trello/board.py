import json
import os

import requests

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(CURRENT_FILE_DIR, "../trello.api"), "r") as f:
    API_KEY = f.read()

with open(os.path.join(CURRENT_FILE_DIR, "../trello.token"), "r") as f:
    API_TOKEN = f.read()

query = {"key": API_KEY, "token": API_TOKEN}

headers = {"Accept": "application/json"}

CARDS_URL = "https://api.trello.com/1/cards"


class Board:
    def __init__(self, id: str):
        self._id = id
        self._lists_url = f"https://api.trello.com/1/boards/{self._id}/lists"

    @property
    def lists_as_json(self) -> dict:
        response = requests.request(
            "GET", self._lists_url, headers=headers, params=query
        )
        return json.loads(response.text)

    def get_list_id_by_name(self, name: str) -> str:
        for val in self.lists_as_json:
            if val["name"] == name:
                return val["id"]

    def add_card_to_list(
        self, list_id: str, name: str, desc: str, card_role: str
    ) -> int:
        add_query = query.copy()
        add_query["idList"] = list_id
        add_query["name"] = name
        add_query["desc"] = desc
        add_query["cardRole"] = card_role

        response = requests.request(
            "POST",
            CARDS_URL,
            headers=headers,
            params=add_query,
        )

        return response.status_code

    def not_already_in_list(self, list_id: str, name: str) -> bool:

        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        response = requests.request("GET", url, headers=headers, params=query)
        if response.status_code == 200:
            cards = json.loads(response.content)
            return not name in [card["name"] for card in cards]
        else:
            raise Exception
