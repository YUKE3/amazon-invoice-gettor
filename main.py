import asyncio
from scrapper import scrapper


async def main():

    async with scrapper() as sc:
        stuff = await sc.getInvoice("---")
        print(stuff)


asyncio.run(main())