import os
from typing import List
import requests
from dotenv import load_dotenv


load_dotenv()
CLICKUP_KEY = os.environ.get('CLICKUP_KEY')


def clickup_query(path : str) -> dict:
    headers = {'Authorization': CLICKUP_KEY}
    response = requests.get("http://api.clickup.com/api/v2" + path, headers=headers)
    return response.json()


# TODO: Error handling
def get_teams() -> List[str]:
    data = clickup_query("/team")
    return [team["id"] for team in data["teams"]]


def get_spaces(team_ids):
    space_ids = []
    for team_id in team_ids:
        data = clickup_query(f"/team/{team_id}/space?archived=false")
        space_ids.extend([space["id"] for space in data["spaces"]])
    return space_ids


def get_folders(space_ids):
    folder_ids = []
    for space_id in space_ids:
        data = clickup_query(f"/space/{space_id}/folder?archived=false")
        folder_ids.extend([folder["id"] for folder in data["folders"]])
    return folder_ids


def get_lists(space_ids, folder_ids):
    list_ids = []
    for space_id in space_ids:
        data = clickup_query(f"/space/{space_id}/list?archived=false")
        list_ids.extend([list["id"] for list in data["lists"]])
    for folder_id in folder_ids:
        data = clickup_query(f"/folder/{folder_id}/list?archived=false")
        list_ids.extend([list["id"] for list in data["lists"]])
    return list_ids


# TODO: Pagination
def get_tasks(list_ids):
    tasks = []
    for list_id in list_ids:
        data = clickup_query(f"/list/{list_id}/task?archived=false&subtasks=true")
        if len(data["tasks"]) > 99:
            print("pagination needed")
        tasks.extend(data["tasks"])
    return tasks


if __name__ == '__main__':
    team_ids = get_teams()
    space_ids = get_spaces(team_ids)
    folder_ids = get_folders(space_ids)
    list_ids = get_lists(space_ids, folder_ids)
    print(get_tasks(list_ids))
