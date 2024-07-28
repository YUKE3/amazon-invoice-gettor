import click
from ..utils.AmazonScrapper import AmazonScrapper 
from ..decorator.coro import coro

@click.command()
@click.argument("email")
@coro
async def login(email):
    asc = AmazonScrapper()

    async with asc(debug=False) as sc:
        await sc.login(email)

        print("Logged in successfully.")
