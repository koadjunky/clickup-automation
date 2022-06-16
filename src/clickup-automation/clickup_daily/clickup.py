import os
from typing import List
import requests
from dotenv import load_dotenv
import pprint


load_dotenv()
CLICKUP_KEY = os.environ.get('CLICKUP_KEY')


# TODO: Error handling
def clickup_get(path : str) -> dict:
    headers = {'Authorization': CLICKUP_KEY}
    response = requests.get("http://api.clickup.com/api/v2" + path, headers=headers)
    return response.json()


# TODO: Error handling
def clickup_put(path: str, data: dict):
    headers = {'Authorization': CLICKUP_KEY}
    requests.put("http://api.clickup.com/api/v2" + path, headers=headers, json=data)


def get_teams() -> List[str]:
    data = clickup_get("/team")
    return [team["id"] for team in data["teams"]]


def get_spaces(team_ids):
    space_ids = []
    for team_id in team_ids:
        data = clickup_get(f"/team/{team_id}/space?archived=false")
        space_ids.extend([space["id"] for space in data["spaces"]])
    return space_ids


def get_folders(space_ids):
    folder_ids = []
    for space_id in space_ids:
        data = clickup_get(f"/space/{space_id}/folder?archived=false")
        folder_ids.extend([folder["id"] for folder in data["folders"]])
    return folder_ids


def get_lists(space_ids, folder_ids):
    list_ids = []
    for space_id in space_ids:
        data = clickup_get(f"/space/{space_id}/list?archived=false")
        list_ids.extend([list["id"] for list in data["lists"]])
    for folder_id in folder_ids:
        data = clickup_get(f"/folder/{folder_id}/list?archived=false")
        list_ids.extend([list["id"] for list in data["lists"]])
    return list_ids


# TODO: Pagination
def get_tasks(list_ids):
    tasks = []
    for list_id in list_ids:
        data = clickup_get(f"/list/{list_id}/task?archived=false&subtasks=true")
        if len(data["tasks"]) > 99:
            print("pagination needed")
        tasks.extend(data["tasks"])
    return tasks


if __name__ == '__main__':
#    team_ids = get_teams() # ['6624359']
#    print(f"Team ids: {team_ids}")
#    space_ids = get_spaces(team_ids)
#    print(f"Space ids: {space_ids}") # ['10877781', '10877784']
#    folder_ids = get_folders(space_ids)
#    print(f"Folder ids: {folder_ids}") # []
#    list_ids = get_lists(space_ids, folder_ids) # ['65455262', '181690923', '198367334', '198386194', '63597033', '65455246', '84170410',
#                                                #  '144556532', '162390920', '181668282', '192354483', '192370658', '192370662']
#    print(f"List ids: {list_ids}")
    pprint.pprint(get_tasks(['181668282']))
