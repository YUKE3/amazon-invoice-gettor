from playwright.async_api import async_playwright, Playwright
import re
import os


class AmazonScrapper:
    def __call__(self, browser="chromium", debug=False):
        self.browser_type = browser
        self.debug = debug
        return self


    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        if self.browser_type == "firefox":
            self.browser = self.playwright.firefox
        else:
            self.browser = self.playwright.chromium

        os.makedirs(r"./accounts", exist_ok=True)
        os.makedirs(r"./invoices", exist_ok=True)

        return self


    async def login(self, email):
        # Separate browser for new login.
        browser = await self.browser.launch(headless=False)
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
        await context.storage_state(path=f"./accounts/{email}.json")
        await page.close()
        await browser.close()


    async def getInvoice(self, order_id):
        browser = await self.browser.launch(headless=not self.debug)
        await self.setupContext(browser)

        # Uses loggedIn state
        context = self.context[0] # TODO: loop through all context
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
        if self.browser_type == "chromium":
            if self.debug: print("[NOTE] Can't download PDF when in debug mode.")
            else: await page.pdf(path=f"invoices/{order_id}.pdf")

        bold_texts = await page.locator("b").all_inner_texts()
        order_total = bold_texts[-12][13:]
        grand_total = bold_texts[-2]
        
        await page.close()
        await browser.close()
        return order_total, grand_total, items


    async def setupContext(self, browser):
        self.context = []

        directory = os.fsencode(r"./accounts")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            context = await browser.new_context(storage_state=f"./accounts/{filename}")
            self.context.append(context)


    async def __aexit__(self, *args):
        await self.playwright.stop()