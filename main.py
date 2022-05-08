def get_all_tasks():
    tasks = []
    with open('task_list.txt') as f:
        for task_line in f.readlines():
            tasks.append(task_line.strip())
    return tasks

def list_tasks(tasks):
    for task in tasks:
        print(task)

list_tasks(get_all_tasks())
