import pendulum
from task import Task
from typing import Callable, Any
from loguru import logger


def safe(func: Callable[..., None]) -> Callable[..., None]:
    """Catches and logs any exception."""

    def wrapper(*args: Any, **kwargs: Any) -> None:
        try:
            return func(*args, **kwargs)
        except:
            logger.exception(f"Exception in function {func.__name__}")

    return wrapper


@safe
def update_due_date(task: Task):
    due_date = task.get_due_date()
    day_start = pendulum.now(tz='Europe/Warsaw').start_of('day')
    if due_date is None or due_date > day_start:
        return
    recurring = task.get_custom_fields().get('recurring', ['false'])
    if 'daily' in recurring:
        due_date = pendulum.now(tz='Europe/Warsaw').at(4, 0, 0)
        task.set_due_date(due_date)
    elif 'weekly' in recurring:
        while due_date < day_start:
            due_date = due_date.add(weeks=1)
        task.set_due_date(due_date)


@safe
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
        update_due_date(Task(task))
        update_status(Task(task))
