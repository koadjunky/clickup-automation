import json
from pathlib import Path
from typing import List
import requests


def get_key():
    config_path = Path.home() / ".config" / "clickup" / "api_token.json"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return config["api_key"]


key = get_key()


def clickup_query(path : str) -> dict:
    headers = {'Authorization': key}
    response = requests.get("http://api.clickup.com/api/v2" + path, headers=headers)
    return response.json()


def get_teams() -> List[str]:
    data = clickup_query("/team")
    return [team["id"] for team in data["teams"]]


def get_spaces(team_ids):
    space_ids = []
    for team_id in team_ids:
        data = clickup_query(f"/team/{team_id}/space?archived=false")
        space_ids.extend([space["id"] for space in data["spaces"]])
    return space_ids


if __name__ == '__main__':
    team_ids = get_teams()
    print(get_spaces(team_ids))
