from .task_controller import task_group, task_new
# from .action_controller import action_group
# from .reports import report_group


import click


@click.group
def group():
  pass


cli = click.CommandCollection(sources=[task_group])
