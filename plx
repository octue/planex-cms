#!/usr/bin/env python
"""
Use `plx --help` to see usage instructions

To make this cli available as an executable on your path, follow this guide:
https://dbader.org/blog/how-to-make-command-line-commands-with-python
"""
import click
from os import system, name


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


# TODO combine install and lock commands using an option, eg install --create-lock wipes and recreates the package lock
@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1)
def install(args):
    """ Runs npm install in the node container
    """
    system(f"docker-compose run node npm install {' '.join(args)}")


@click.command()
def lock():
    """ Recreates package-lock.json file recording the exact freeze of the installation in plx_node container.
    This is critical following any change to the package.json file, since the lock file tightens exact
    versions of packages.
    """
    if name == "nt":
        system("del -f package-lock.json && docker-compose run node npm install --package-lock-only")
    else:
        system("rm -f package-lock.json && docker-compose run node npm install --package-lock-only")


@click.command()
@click.argument("args", nargs=-1)
def manage(args):
    """ Invoke a django management command in the server container.
    """
    arg_string = " ".join(args)
    system(f"docker-compose run web python manage.py {arg_string}")


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
    test_spec = " ".join(args) if len(args) >= 1 else "backend/test"
    system(f"docker-compose run web python manage.py test {test_spec}")


cli.add_command(build)
cli.add_command(dev)
cli.add_command(install)
cli.add_command(lock)
cli.add_command(manage)
cli.add_command(stop)
cli.add_command(test)


if __name__ == "__main__":
    cli()
