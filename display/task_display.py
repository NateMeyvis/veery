from typing import List

from objects.task import Task

def task_ordered_list(tasks: List[Task]) -> str:
    """Given a list of tasks, return an HTML ordered list of them."""
    result = "<ol>"
    for task in tasks:
        result += f"<li>{str(task)}</li>"
    result += "</ol>"
    return result

def task_display(tasks: List[Task]) -> str:
    """Given a list of tasks, return HTML to display them."""
    return f"""
        <html>
        <head>
            <title>Veery</title>
        <head>
        <body>
            {task_ordered_list(tasks)}
        </body>
        </html>
    """
