import click

@click.command()
@click.argument("email")
def logout(email):
    click.echo(f"This is the logout command! {email}")