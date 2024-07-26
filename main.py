from playwright.async_api import async_playwright, Playwright
import asyncio
import re


async def main():
    async with async_playwright() as playwright:
        firefox = playwright.firefox
        browser = await firefox.launch(headless = False)

        # loginPage = asyncio.create_task(login(browser, "neia@duck.com"))
        # await loginPage

        invc = asyncio.create_task(getInvoice(browser, "..."))
        await invc

        await browser.close()


async def login(browser, email):
    # Separate context for new login.
    context = await browser.new_context()
    page = await context.new_page()
    
    # Navigates to password screen.
    await page.goto("https://amazon.com")
    await page.click("#nav-link-accountList")
    await page.get_by_label("Email or mobile phone number ").fill(email)
    await page.get_by_role("button", name="Continue").click()
    await page.get_by_label("Keep me signed in.").check()
    
    # Waits until logged in.
    await page.wait_for_url(re.compile(r"^(^(https:\/\/www.amazon.com\/\?ref_=nav_ya_signin).*).*"), timeout=300000)
    
    # Saves storage state
    await context.storage_state(path="account.json")
    await page.close()


async def getInvoice(browser, order_id):
    # Uses loggedIn state
    context = await browser.new_context(storage_state='account.json')
    page = await context.new_page()
    
    # Go to your orders page
    await page.goto("https://www.amazon.com/gp/your-account/order-history")
    await page.get_by_placeholder("Search all orders").fill(order_id)
    await page.get_by_role("button", name="Search Orders").click()
    await page.get_by_role("link", name="View invoice").click()

    # Waits for page to laod.
    await page.wait_for_load_state("networkidle")

    # Get the names of the items
    items = (await page.locator("i").all_inner_texts())

    # Download the invoice
    # only in headless chromium
    # await page.pdf(path=f"invoices/{order_id}.pdf")

    bold_texts = await page.locator("b").all_inner_texts()
    order_total = bold_texts[-12][13:]
    grand_total = bold_texts[-2]
    
    await page.close()
    return order_total, grand_total, items


asyncio.run(main())

print("Hello Amazon!")