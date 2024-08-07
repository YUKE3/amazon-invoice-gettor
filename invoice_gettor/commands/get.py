import click
import decimal
import os
import datetime
from dotenv import load_dotenv
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
    load_dotenv()
    if gpt:
        if "OPENAI_API_KEY" not in os.environ:
            print(f"Please add \"OPENAI_API_KEY\" to .env to use --gpt")
            return
    if actual:
        env_vars = ["base_url", "password", "encryption_password", "file", "account"]
        missing = False
        for var in env_vars:
            if var not in os.environ:
                print(f"Please add \"var\" to .env to use --actual")
                missing = True
        if missing: return
    
    asc = AmazonScrapper()

    async with asc(debug=debug) as sc:
        order_total, grand_total, items = await sc.getInvoice(order_id)
        if not order_total:
            print(f"Order not found in valid accounts.")
            return 

            
        print(f"Order ID: {order_id}")
        print("--------------------------------")
        print("Items in invoice:")
        for i, names in enumerate(items):
            print(f"{i+1}. {names}")
        print("--------------------------------")
        print(f"Order total: {order_total}  Grand total: {grand_total}")
        print("--------------------------------")

        if gpt:
            try:
                gptw = GPTWrapper()
                shortened_names = gptw.summarizeOrder(items)

                print("Summarized items:")
                for i, names in enumerate(shortened_names):
                    print(f"{i+1}. {names}")
            except Exception as e:
                if hasattr(e, 'message'):
                    message = e.message
                else:
                    message = e
                print(f"[ERROR] GPT integration failed with error:\n{message}")
                gpt = False
            
            print("--------------------------------")

        if actual:
            if gpt:
                notes = ", ".join(shortened_names) + " | " + order_id
            else:
                notes = order_id

            print("New Actual transaction details:")
            print(notes)

            while True:
                date = input("Date of this transaction? [YYYY/MM/DD (year is optional)] (empty for today):")
                print(date)
                if date == '':
                    print(date)
                    date = datetime.datetime.now()
                    break

                date = date.split('/')
                if len(date) < 3: # Add year if not specified
                    date.insert(0,datetime.datetime.now().date().strftime('%Y'))
                try:
                    date = datetime.date(*map(int, date))
                    break
                except Exception as e:
                    print(f"[ERROR] Please enter a valid date.")

            confirmation = input("Add this transaction? (yes/no):")
            if confirmation.lower() == 'yes' or confirmation.lower() == 'y' or confirmation == '':
                try:
                    with ActualWrapper() as aw:
                        aw.addOrder(notes=notes, payment=decimal.Decimal("-"+order_total[1:]), date=date, category="")
                        print("Transactiona added successfully.")
                except Exception as e:
                    if hasattr(e, 'message'):
                        message = e.message
                    else:
                        message = e
                    print(f"[ERROR] Actual integration failed with error:\n{message}")