import pendulum

class Task:

    def __init__(self, data: dict):
        self.data = data
        self.updates = {}

    # TODO: Generic accessor method
    def get_id(self):
        return self.data.get('id', None)

    def get_name(self):
        return self.data.get('name', 'UNKNOWN')

    def get_old_status(self):
        return self.data.get('status', {}).get('status', 'UNKNOWN')

    def get_new_status(self):
        return self.updates.get('status', 'NOT SET')

    def is_dirty(self):
        return bool(self.updates)

    def get_status(self):
        if 'status' in self.updates:
            return self.get_new_status()
        return self.get_old_status()

    def set_status(self, status):
        name = self.get_name()
        id = self.get_id()
        if 'status' in self.updates and status == self.get_old_status():
            print(f"Clearing status of task: {name}")
            del self.updates['status']
        if status != self.get_old_status():
            print(f"Setting status '{status}' of task: {name}, id: {id}")
            self.updates['status'] = status

    def get_start_date(self):
        timestamp = self.data.get("start_date", None)
        return Task.__ts_to_dt(timestamp)

    def get_due_date(self):
        timestamp = self.updates.get('due_date', self.data.get('due_date', None))
        return Task.__ts_to_dt(timestamp)

    def set_due_date(self, dt: pendulum.DateTime) -> None:
        name = self.get_name()
        timestamp = Task.__dt_to_ts(dt)
        if 'due_date' in self.updates and timestamp == self.data.get('due_date', None):
            print(f"Clearing due date of task: {name}")
            del self.updates['due_date']
            del self.updates['due_date_time']
        if timestamp != self.data.get('due_date', None):
            print(f"Setting due date of task: {name} to {dt}")
            self.updates['due_date'] = timestamp
            self.updates['due_date_time'] = False

    def get_custom_fields(self):
        result = {}
        for field in self.data.get('custom_fields', []):
            name = field.get('name', 'UNKNOWN')
            options = {}
            for option in field.get('type_config', {}).get('options', []):
                if 'label' in option: options[option['id']] = option['label']
            value = []
            for option_id in field.get('value', []):
                if option_id in options:
                    value.append(options[option_id])
            result[name] = value
        return result

    @staticmethod
    def __ts_to_dt(timestamp: int) -> pendulum.DateTime:
        if timestamp is None:
            return None
        return pendulum.from_timestamp(int(timestamp) // 1000, tz='Europe/Warsaw')

    @staticmethod
    def __dt_to_ts(dt: pendulum.DateTime):
        return str(dt.int_timestamp * 1000)


if __name__ == '__main__':
    TASK_DATA = {
        'id': '2cwtuap',
        'custom_id': None,
        'name': 'Bike',
        'text_content': '',
        'description': '', 
        'status': {
            'id': 'sc181668282_0sWtjYW1',
            'status': 'today',
            'color': '#e50000',
            'orderindex': 2,
            'type': 'custom'
        },
        'orderindex': '0.00000108000000000000000000000000',
        'date_created': '1650713085596',
        'date_updated': '1655968704447',
        'date_closed': None,
        'archived': False,
        'creator': {
            'id': 4721539,
            'username': 'Maciej Małycha',
            'color': '#0388d1',
            'email': 'm.malycha@gmail.com',
            'profilePicture': None
        },
        'assignees': [{
            'id': 4721539,
            'username': 'Maciej Małycha',
            'color': '#0388d1',
            'initials': 'MM',
            'email': 'm.malycha@gmail.com',
            'profilePicture': None
        }],
        'watchers': [{
            'id': 4721539,
            'username': 'Maciej Małycha',
            'color': '#0388d1',
            'initials': 'MM',
            'email': 'm.malycha@gmail.com',
            'profilePicture': None
        }], 
        'checklists': [],
        'tags': [],
        'parent': None,
        'priority': {
            'id': '2',
            'priority': 'high',
            'color': '#ffcc00',
            'orderindex': '2'
        },
        'due_date': '1655949600000',
        'start_date': '1655848800000',
        'points': None,
        'time_estimate': 5400000,
        'time_spent': 0,
        'custom_fields': [{
            'id': 'd84460e5-c4e9-4573-9e8e-390e17ab096c',
            'name': 'recurring',
            'type': 'labels',
            'type_config': {
                'options': [{
                    'id': '5d1d9862-e7be-41f5-8f98-f5d4be520630',
                    'label': 'daily',
                    'color': None
                }, {
                    'id': '78114803-1cf9-48f7-90fb-cebd793a1785',
                    'label': 'weekly',
                    'color': None
                }, {
                    'id': '7c02425a-01ed-4f27-a99f-e21b0a016730',
                    'label': 'monthly',
                    'color': None
                }]
            },
            'date_created': '1655404950619',
            'hide_from_guests': False,
            'value': ['5d1d9862-e7be-41f5-8f98-f5d4be520630'],
            'required': False
        }],
        'dependencies': [],
        'linked_tasks': [],
        'team_id': '6624359',
        'url': 'https://app.clickup.com/t/2cwtuap',
        'permission_level': 'create',
        'list': {
            'id': '181668282',
            'name': 'Recurring',
            'access': True
        },
        'project': {
            'id': '103613428',
            'name': 'hidden',
            'hidden': True,
            'access': True
        },
        'folder': {
            'id': '103613428',
            'name': 'hidden',
            'hidden': True,
            'access': True
        },
        'space': {
            'id': '10877784'
        },
        'attachments': []
    }
    task = Task(TASK_DATA)
    # It seems, we cannot distinguish due_date and due_date_time at 4:00 local time (2:00 UTC)
    print(task.get_start_date())
    print(task.get_due_date())
    print("Should be today:", task.get_status())
    print("Should be not dirty:", task.is_dirty())
    task.set_status('this week')
    print("Should be this week:", task.get_status())
    print("Should be dirty:", task.is_dirty())
    task.set_status('today')
    print("Should be today:", task.get_status())
    print("Should be not dirty:", task.is_dirty())

    print("Get custom fields, should be recurring daily:", task.get_custom_fields())

    print("Should be 2022-06-23 04:00 CEST:", task.get_due_date())
    print("Should be not dirty:", task.is_dirty())
    task.set_due_date(pendulum.now())
    print("Should be now: ", task.get_due_date())
    print("Should be dirty:", task.is_dirty())
    task.set_due_date(pendulum.parse('2022-06-23T04:00:00+02:00'))
    print("Should be 2022-06-23 04:00 CEST:", task.get_due_date())
    print("Should be not dirty:", task.is_dirty())

