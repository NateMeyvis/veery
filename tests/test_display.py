from display.task_display import task_display


def test_task_display(tasks):
    generated_html = task_display("dummy_env", tasks)
    for task in tasks:
        assert task.description in generated_html
