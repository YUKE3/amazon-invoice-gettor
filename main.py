from playwright.async_api import async_playwright, Playwright
import asyncio
import re


async def main():
    async with async_playwright() as playwright:
        firefox = playwright.firefox
        browser = await firefox.launch(headless = False)

        loginPage = asyncio.create_task(login(browser, "neia@duck.com"))
        await loginPage

        invc = asyncio.create_task(getInvoice(browser))
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


async def getInvoice(browser):
    context = await browser.new_context(storage_state='account.json')
    page = await context.new_page()
    await page.goto("https://amazon.com/")
    await page.wait_for_timeout(10000)


asyncio.run(main())

print("Hello Amazon!")