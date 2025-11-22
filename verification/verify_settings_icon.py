
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000")

        # Wait for settings to load and be visible
        try:
            page.wait_for_selector(".setting-row-label", timeout=10000)
        except:
            print("Timeout waiting for .setting-row-label. Taking screenshot anyway.")

        # Click on the first category to expand it and show settings
        try:
            page.click(".category-header", timeout=5000)
            page.wait_for_selector(".setting-row", state="visible", timeout=5000)
        except:
             print("Could not expand category or find visible settings.")

        page.screenshot(path="/home/jules/verification/settings_icon_verification.png")
        browser.close()

if __name__ == "__main__":
    run()
