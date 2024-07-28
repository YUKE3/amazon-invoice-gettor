import click
from invoice_gettor.commands import get, login, logout

@click.group()
def cli():
    pass

cli.add_command(get.get)
cli.add_command(login.login)
cli.add_command(logout.logout)

if __name__ == '__main__':
    cli()