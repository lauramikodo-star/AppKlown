
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000")

        # Wait for the config container to have children (meaning categories are rendered)
        # or wait for the loading message to disappear
        try:
            page.wait_for_selector(".category", timeout=10000)
        except:
            print("Timeout waiting for .category. Taking screenshot anyway.")

        page.screenshot(path="/home/jules/verification/folder_icon_verification.png")
        browser.close()

if __name__ == "__main__":
    run()
