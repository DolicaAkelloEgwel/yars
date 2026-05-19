import json

import requests

with open("trello.api", "r") as f:
    API_KEY = f.read()

with open("trello.token", "r") as f:
    API_TOKEN = f.read()

query = {"key": API_KEY, "token": API_TOKEN}

headers = {"Accept": "application/json"}

CARDS_URL = "https://api.trello.com/1/cards"


class Board:
    def __init__(self, id: str):
        self._id = id
        self._lists_url = f"https://api.trello.com/1/boards/{self._id}/lists"

    @property
    def lists_url(self) -> str:
        return self._lists_url

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
