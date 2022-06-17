import pendulum
from task import Task

def update_status(task: Task):
    now = pendulum.now(tz="Europe/Warsaw")
    day_end = now.end_of('day')
    week_end = now.end_of('week')
    if task.get_start_date() is not None and task.get_start_date() < now:
        task.set_status("today")
    elif task.get_due_date() is not None and task.get_due_date() < day_end:
        task.set_status("today")
    elif task.get_start_date() is not None and task.get_start_date() < week_end:
        task.set_status("this week")
    elif task.get_due_date() is not None and task.get_due_date() < week_end:
        task.set_status("this week")

if __name__ == "__main__":
    from clickup import get_teams, get_spaces, get_folders, get_lists, get_tasks
    team_ids = get_teams()
    space_ids = get_spaces(team_ids)
    folder_ids = get_folders(space_ids)
    list_ids = get_lists(space_ids, folder_ids)
    tasks = get_tasks(list_ids)
    for task in tasks:
        update_status(Task(task))
