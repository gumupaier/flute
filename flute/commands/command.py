# -*- coding: utf-8 -*-
# @Time    : 2020/12/11 9:30 下午
# @File    : command.py
import click

from flute.apps.amber.task import StackfileGenerator


@click.command()
@click.argument('arg')
def main(arg):
    if arg == 'amber':
        sg = StackfileGenerator()
        sg.process()
    else:
        click.echo("Command is under development")


if __name__ == '__main__':
    main()
