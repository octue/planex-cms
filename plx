#!/usr/bin/env python
"""
Use `plx --help` to see usage instructions

To make this cli available as an executable on your path, follow this guide:
https://dbader.org/blog/how-to-make-command-line-commands-with-python
"""
from os import system
import click


@click.group()
def cli():
    """
    A command line utility to aid in local development using docker-compose,
    to save ridiculous amounts of typing cranky commands.

    This is not intended for use in ci/cd or production, where you only have to
    type commands once in your setup ;)
    """
    pass


@click.command()
def build():
    """Build the docker images specified in the docker-compose file.

    This will install relevant requirements into the image, so needs to be done after modifying
    the requirements.txt file, for example.
    """
    system("docker-compose build")


@click.command()
def dev():
    """ Run a hot reloading server for local development.
    Do not use in production, as this uses django's runserver.
    """
    system("docker-compose up")


@click.command()
@click.argument("args", nargs=-1)
def manage(args):
    """ Invoke a django management command in the server container.
    """
    arg_string = " ".join(args)
    system(f"docker-compose run web python manage.py {arg_string}")


@click.command()
@click.option(
    "--with-volumes",
    is_flag=True,
    default=False,
    show_default=True,
    help="Purge all volumes related to planex-cms containers (postgres, pgadmin, etc). HIGHLY DESTRUCTIVE.",
)
def prune(with_volumes):
    """ Find and destroy all windquest containers, optionally removing their persistent volumes

    See https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes#a-docker-cheat-sheet

    """
    volume_flag = "-v" if with_volumes else ""
    # Flake8 has to be ignored because grep's escape characters are valid but flake thinks it's python
    system("docker ps -a | grep 'plx_\|planex_' | awk '{print $1}' | xargs docker rm %s" % volume_flag)  # noqa:W605


@click.command()
def stop():
    """ Stop any running containers
    """
    system("docker-compose stop")


@click.command()
@click.argument("args", nargs=-1)
def test(args):
    """ Run django tests in the server container. By default runs all tests in backend/test folder.
    Individual tests or classes can be specified as an argument, e.g.
     plx test test.test_users.UsersTestCase runs all tests in the UsersTestCase class.
    """
    test_spec = " ".join(args) if len(args) >= 1 else "planex/test"
    system(f"docker-compose run web python manage.py test {test_spec}")


cli.add_command(build)
cli.add_command(dev)
cli.add_command(manage)
cli.add_command(prune)
cli.add_command(stop)
cli.add_command(test)


if __name__ == "__main__":
    cli()
