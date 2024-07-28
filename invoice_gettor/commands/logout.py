import click
from ..utils.AmazonScrapper import AmazonScrapper 
from ..decorator.coro import coro

@click.command()
@click.argument("email")
@coro
async def logout(email):
    # TODO: add option to logout all

    click.echo(f"This is the logout command! {email}")
    
    # Goes through account and press "logout"

