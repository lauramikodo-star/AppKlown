
from playwright.sync_api import sync_playwright, expect

def verify_cloning_mode_dialog():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app
        page.goto("http://localhost:8000/index.html")

        # Wait for the configuration to load
        page.wait_for_selector("#config-container .category", timeout=10000)

        # Open the "Cloning Options" category first if needed, or just search for the text.
        # The error said there are 2 elements. One might be in the dialog itself if it was already open?
        # Or maybe duplicate settings?
        # Let's try to narrow it down to the setting row.

        # Expand "Cloning Options" category.
        # Assuming "Cloning Mode" is in "Cloning Options" category.
        cloning_options_header = page.get_by_text("Cloning Options")
        if cloning_options_header.count() > 0:
            cloning_options_header.first.click()

        # Use first() because get_by_text found duplicates.
        # We want the one that is visible and clickable in the main list.
        cloning_mode_row = page.get_by_text("Cloning Mode", exact=True).first
        cloning_mode_row.click()

        # Wait for the floating editor overlay to be visible
        page.wait_for_selector("#floating-editor-overlay.visible")

        # Verify the dialog title
        expect(page.locator("#floating-editor-header")).to_have_text("Cloning Mode")

        # Verify the Dropdown exists (Cloning Mode)
        expect(page.locator("#floating-editor-body select")).to_be_visible()

        # Verify the Child Setting "Manifest Compatibility Mode" exists
        manifest_mode_checkbox = page.get_by_label("Manifest Compatibility Mode")
        expect(manifest_mode_checkbox).to_be_visible()

        # Take a screenshot
        page.screenshot(path="/app/verification/cloning_mode_dialog.png")

        browser.close()

if __name__ == "__main__":
    verify_cloning_mode_dialog()
