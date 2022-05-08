def get_all_tasks():
    tasks = []
    with open('task_list.txt') as f:
        for task_line in f.readlines():
            tasks.append(task_line.strip())
    return tasks

def list_tasks(tasks):
    for task in tasks:
        print(task)

def set_task_list(tasks):
    with open('task_list.txt', 'w') as f:
        f.write('\n'.join(tasks))

def add_task(new_task):
    task_list = get_all_tasks()
    task_list.append(new_task)
    set_task_list(task_list)

def remove_task(task_to_remove):
    task_list = get_all_tasks()
    task_list = [task for task in task_list if task != task_to_remove]
    set_task_list(task_list)

