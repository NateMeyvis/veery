from typing import List

from objects.task import Task

def task_ordered_list(tasks: List[Task]) -> str:
    """Given a list of tasks, return an HTML ordered list of them."""
    result = "<ol>"
    for task in tasks:
        result += f"<li>{str(task)}</li>"
    result += "</ol>"
    return result

def add_task_form() -> str:
    return """<form action="/add" method="post">
        Description: <input type="text" name="description" />
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
