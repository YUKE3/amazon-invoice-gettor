import click
import decimal
from ..utils.AmazonScrapper import AmazonScrapper
from ..utils.GPTWrapper import GPTWrapper
from ..utils.ActualWrapper import ActualWrapper
from ..decorator.coro import coro

@click.command()
@click.argument("order_id")
@click.option('--gpt', is_flag=True, default=False, help="Enable GPT summarization.")
@click.option('--actual', is_flag=True, default=False, help="Enable Actual Integration.")
@click.option('--no_pdf', is_flag=True, default=False, help="Don't download PDF.")
@click.option('--debug', is_flag=True, default=False, help="Shows browser (disables PDF downloading)")
@coro
async def get(gpt, actual, no_pdf, debug, order_id):
    asc = AmazonScrapper()

    async with asc(debug=debug) as sc:
        # TODO: Check env associated with flags


        order_total, grand_total, items = await sc.getInvoice(order_id)
        print(items)
        print(order_total)

        if gpt:
            gptw = GPTWrapper()
            shortened_names = gptw.summarizeOrder(items)
        
        print("Summarized items:")
        print(shortened_names)

        if actual:
            notes = ", ".join(shortened_names) + " | " + order_id
            print(notes)
            with ActualWrapper() as aw:
                aw.addOrder(notes=notes, payment=decimal.Decimal("-"+order_total[1:]), date="", category="")