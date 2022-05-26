from typing import List

from objects.task import Task


def completion_button(task):
    return f"""<form action='/complete/{task.uuid.hex}' method='post'>
            <label for='Mark {task.uuid.hex} complete'>{str(task)}</label>
            <input type='submit' id='Mark {task.uuid.hex} complete' value='Mark complete' /></form>"""

def kick_button(task):
    return f"""<form action='/kick/{task.uuid.hex}' method='post'>
            <label for='Kick {task.uuid.hex}'>Kick</label>
            <input type='submit' id='Kick {task.uuid.hex}' value='Kick' /></form>"""


def task_ordered_list(tasks: List[Task]) -> str:
    """Given a list of tasks, return an HTML ordered list of them."""
    result = "<ol>"
    for task in tasks:
        result += f"<li>{completion_button(task)} {kick_button(task)}</li>"
    result += "</ol>"
    return result


def add_task_form() -> str:
    return """<form action="/add" method="post">
        Description: <input type="text" name="description" />
        <br>
        Due (leave blank for None): <input type="datetime-local" name="due" />
        <input type='submit' value='Add task' />
    </form>"""


def task_display(tasks: List[Task]) -> str:
    """Given a list of tasks, return HTML to display them."""
    return f"""
        <html>
        <head>
            <title>Veery</title>
        <head>
        <body>
            {task_ordered_list(tasks)}
            <br>
            {add_task_form()}
        </body>
        </html>
    """
