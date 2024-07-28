import click
from ..utils.AmazonScrapper import AmazonScrapper 
from ..decorator.coro import coro

@click.command()
@click.argument("email")
@click.option('--debug', is_flag=True, default=False, help="Shows browser")
@coro
async def logout(email, debug):
    # TODO: add option to logout all

    # Goes through account and press "logout"
    asc = AmazonScrapper()

    async with asc(debug=debug) as sc:
        try:
            await sc.logout(email)
            print("Logged out successfully.")
        except Exception as e:
            print(e)
            print("Please try again.")