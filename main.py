from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context()
        pg = ctx.new_page()
        pg.goto("https://amazon.com")
        pg.wait_for_timeout(1000)
        browser.close()

main()

print("Hello Amazon!")