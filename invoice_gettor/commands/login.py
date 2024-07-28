import click

@click.command()
@click.argument("email")
def login(email):
    click.echo(f"This is the login command! {email}")