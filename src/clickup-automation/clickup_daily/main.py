from clickup import get_all_tasks, update_task
from task import Task
from strategies import update_status, update_due_date, safe
from discord import send


def main():
    task_dicts = get_all_tasks()
    tasks = [Task(task_dict) for task_dict in task_dicts]
    for task in tasks:
        process_task(task)


@safe
def process_task(task: Task):
    update_due_date(task)
    update_status(task)
    if task.is_dirty():
        if 'due_date' in task.updates:
            send(f"Adjusting due date of recurring task: '{task.get_name()}'")
        if 'status' in task.updates:
            send(f"Updating task: '{task.get_name()}' from status '{task.get_old_status()}' to status '{task.get_new_status()}'.")
        update_task(task.get_id(), task.updates)


if __name__ == '__main__':
    main()
