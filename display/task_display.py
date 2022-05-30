from typing import List

from objects.task import Task

FONT_CSS = "<link href='http://fonts.googleapis.com/css?family=Work+Sans' rel='stylesheet' type='text/css'>"

BASE_CSS = f"""<style>
            body {{
                font-family: 'Work Sans';
                background-color: lightgrey;
            }}
            input {{
                display: inline-block;
                color: blue;
            }}
            .button {{
                display: inline-block;
            }}
            .task {{
                display: inline-block;
            }}
            .main-task {{
                max-width: 825px;
                margin-left: auto;
                margin-right: auto;
                margin-top: 100px;
            }}
            .overdue {{
                background-color: pink;
            }}
            .stale {{
                background-color: lightbrown;
            }}
            </style>
        """


def class_list_for_task(task: Task) -> str:
    class_names = ["task"]
    if task.overdue:
        class_names.append("overdue")
    if task.stale:
        class_names.append("stale")
    return " ".join(class_names)


def completion_button(task: Task) -> str:
    return f"""<form class='completion button' action='/complete/{task.uuid.hex}' method='post'>
            <label for='Mark {task.uuid.hex} complete'>{str(task)}</label>
            <input type='submit' id='Mark {task.uuid.hex} complete' value='Mark complete' /></form>"""


def kick_button(task):
    return f"""<form class='kick button' action='/kick/{task.uuid.hex}' method='post'>
            <input type='submit' id='Kick {task.uuid.hex}' value='Kick' /></form>"""


def li_for_task(task):
    return f"""
        <li><div class='{class_list_for_task(task)}' id='task-{task.uuid.hex}'>{completion_button(task)}{kick_button(task)}</div></li>
    """


def task_ordered_list(tasks: List[Task]) -> str:
    """Given a list of tasks, return an HTML ordered list of them."""
    result = "<ol class='task-list'>"
    result += "".join([li_for_task(task) for task in tasks])
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
            {FONT_CSS}
            {BASE_CSS}
        </head>
        <body>
            <div class='main-task'>
                {task_ordered_list(tasks)}
                <br>
                {add_task_form()}
            </div>
        </body>
        </html>
    """
