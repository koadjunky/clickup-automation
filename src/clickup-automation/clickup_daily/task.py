import pendulum

class Task:

    def __init__(self, data: dict):
        self.data = data

    def get_start_date(self):
        timestamp = self.data["start_date"]
        return Task.__ts_to_dt(timestamp)

    def get_due_date(self):
        timestamp = self.data["due_date"]
        return Task.__ts_to_dt(timestamp)

    @staticmethod
    def __ts_to_dt(timestamp):
        if timestamp is None:
            return None
        return pendulum.from_timestamp(int(timestamp) // 1000)


if __name__ == '__main__':
    TASK_DATA = {
        'archived': False,
        'assignees': [{
            'color': '#0388d1',
            'email': 'm.malycha@gmail.com',
            'id': 4721539,
            'initials': 'MM',
            'profilePicture': None,
            'username': 'Maciej Małycha'
        }],
        'checklists': [],
        'creator': {
            'color': '#0388d1',
            'email': 'm.malycha@gmail.com',
            'id': 4721539,
            'profilePicture': None,
            'username': 'Maciej Małycha'
        },
        'custom_fields': [],
        'custom_id': None,
        'date_closed': None,
        'date_created': '1654759466345',
        'date_updated': '1655259097674',
        'dependencies': [],
        'description': None,
        'due_date': '1655344800000',
        'folder': {
            'access': True,
            'hidden': True,
            'id': '31952458',
            'name': 'hidden'
        },
        'id': '2katdb8',
        'linked_tasks': [],
        'list': {'access': True, 'id': '65455262', 'name': 'Other'},
        'name': 'VPN',
        'orderindex': '2885.00123976000000000000000000000000',
        'parent': None,
        'permission_level': 'create',
        'points': None,
        'priority': None,
        'project': {
            'access': True,
            'hidden': True,
            'id': '31952458',
            'name': 'hidden'
        },
        'space': {'id': '10877781'},
        'start_date': '1655251200000',
        'status': {
            'color': '#e50000',
            'orderindex': 2,
            'status': 'today',
            'type': 'custom'
        },
        'tags': [],
        'team_id': '6624359',
        'text_content': None,
        'time_estimate': None,
        'url': 'https://app.clickup.com/t/2katdb8',
        'watchers': []
    }
    task = Task(TASK_DATA)
    # It seems, we cannot distinguish due_date and due_date_time at 4:00 (or 2:00 UTC)
    print(task.get_start_date())
    print(task.get_due_date())
