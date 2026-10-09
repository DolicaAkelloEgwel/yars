import json
import logging
import os

import requests
from auth import get_access_token

headers = {"Accept": "application/json", "Authorization": f"Bearer {get_access_token()}"}

CARDS_URL = "https://api.trello.com/1/cards"


class Board:
    def __init__(self, id: str):
        self._id = id
        self._lists_url = f"https://api.trello.com/1/boards/{self._id}/lists"

    @property
    def lists_as_json(self) -> dict:
        response = requests.request(
            "GET", self._lists_url, headers=headers
        )
        print(response.status_code)
        print(response.text)
        return json.loads(response.text)

    def get_list_id_by_name(self, name: str) -> str:
        for val in self.lists_as_json:
            if val["name"] == name:
                return val["id"]

    def add_card_to_list(
        self, list_id: str, name: str, desc: str, card_role: str
    ) -> int:
        add_query = dict()
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
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            cards = json.loads(response.content)
            return not name in [card["name"] for card in cards]
        else:
            raise Exception
