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
        print("Items in invoice:")
        for i, names in enumerate(items):
            print(f"{i}. {names}")
        print("--------------------------------")
        print(f"Order total: {order_id}  Grand total: {grand_total}")

        if gpt:
            gptw = GPTWrapper()
            shortened_names = gptw.summarizeOrder(items)
        
            print("Summarized items:")
            for i, names in enumerate(shortened_names):
                print(f"{i}. {names}")
            print("--------------------------------")

        if actual:
            if gpt:
                notes = ", ".join(shortened_names) + " | " + order_id
            else:
                notes = order_id

            print("New Actual transaction:")
            print(notes)
            confirmation = input("Add this transaction? (yes/no):")
            if confirmation.lower() == 'yes' or confirmation.lower() == 'y':
                with ActualWrapper() as aw:
                    aw.addOrder(notes=notes, payment=decimal.Decimal("-"+order_total[1:]), date="", category="")
            else:
                pass