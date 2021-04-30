import datetime
import shutil
from os import get_terminal_size, path, system

import click

APPLICATION_NAME = "Hagrid"
COLUNS_TERMINAL = get_terminal_size().columns


@click.group()
def cli():
    message = ' Eu confiaria meus repositórios à Hagrid! '
    print('='*COLUNS_TERMINAL)
    print(' ' * ((COLUNS_TERMINAL - len(message))//2) + message)
    print('='*COLUNS_TERMINAL)
    print('\n')

@cli.command()
@click.option("--folder", "-f", type=click.Path(exists=True))
def add(folder):
    if path.exists(f"{folder}/.git") is False:
        click.echo("❌ A pasta indicada não possui um repositório")
        exit()

    with open("repositories.txt", "r+") as file:
        text = file.read()

        if folder in text:
            click.echo("❎ Repositório já registrado")
            print('\n')
            exit()

        file.write(f"{folder}\n")
        click.echo("✅ Repositório registrado! ")
        print('\n')


@cli.command()
def remove():
    pass


@cli.command()
def status():
    file = open("repositories.txt", "r")
    total_repositories = 0
    total_commited = 0

    for line in file.readlines():
        total_repositories += 1

        folder = line.strip()
        base_command = f"git --git-dir={folder}/.git --work-tree={folder}"
        uncommited_command = f"{base_command} diff-index --quiet HEAD --"

        output = system(uncommited_command)

        if output == 0:
            total_commited += 1
            click.echo(f"😎 Repositório {folder} atualizado!")
        else:
            click.echo(f"😖 Repositório {folder} com arquivos pendentes")

    click.echo(f"{total_commited} dos {total_repositories} estão commitados 😉")


@cli.command()
def sync():
    today = datetime.datetime.now().strftime("%d %a, %b of %Y at %H:%M")

    file = open("repositories.txt", "r")
    for line in file:
        folder = line.strip()
        base_command = f"git --git-dir={folder}/.git --work-tree={folder}"
        uncommited_command = f"{base_command} diff-index --quiet HEAD --"
        push_command = f"{base_command} push"
        commit_command = f'{base_command} commit -am "Forced commit by {APPLICATION_NAME} in {today}"'

        output = system(uncommited_command)

        if output == 0:
            click.echo(f"Repositório {folder} atualizado!")
            system(push_command)
        else:
            click.echo(f"Repositório {folder} com arquivos pendentes")
            system(commit_command)
            system(push_command)

        click.echo('\n')


if __name__ == "__main__":
    cli()
