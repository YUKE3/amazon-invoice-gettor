import asyncio
from AmazonScrapper import AmazonScrapper
from GPTWrapper import GPTWrapper
from ActualWrapper import ActualWrapper
import decimal


async def main():
    gpt = GPTWrapper()
    scc = AmazonScrapper()

    async with scc(debug=False) as sc:
        # await sc.login("neia@duck.com")
        order_id = "111-9886129-5664243"
        order_total, grand_total, items = await sc.getInvoice(order_id)
        print(items)
        # shortened_names = gpt.summarizeOrder(items)
        # notes = ", ".join(shortened_names) + " | " + order_id
        # with ActualWrapper() as aw:
        #     aw.addOrder(notes=notes, payment=decimal.Decimal("-"+order_total[1:]), date="", category="")
        print("End")


asyncio.run(main())