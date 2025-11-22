
from playwright.sync_api import sync_playwright, expect

def verify_external_storage_settings():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app
        page.goto("http://localhost:8000/index.html")

        # Wait for the configuration to load
        page.wait_for_selector("#config-container .category", timeout=10000)

        # Expand "Storage Options" category if needed.
        # We don't know the exact category name for "redirectExternalStorage",
        # so we'll search for the setting label globally.
        # "Redirect External Storage"

        # Since the category might be collapsed, we might need to find which category it belongs to.
        # But `handleSearch` logic in the app shows how it finds things.
        # We can use the search bar to filter!

        page.fill("#search-input", "redirect external storage")
        page.wait_for_timeout(500) # Wait for filter

        # Now the setting should be visible
        setting_row = page.get_by_text("Redirect External Storage").first
        expect(setting_row).to_be_visible()

        # Click to open editor
        setting_row.click()

        # Wait for editor
        page.wait_for_selector("#floating-editor-overlay.visible")
        expect(page.locator("#floating-editor-header")).to_have_text("Redirect External Storage")

        # Find the main toggle
        # It's a checkbox with id based on data path.
        # We can look for the label "Redirect External Storage" inside the editor body
        # The parent toggle label usually matches the setting name.
        editor_body = page.locator("#floating-editor-body")
        toggle_label = editor_body.get_by_text("Redirect External Storage", exact=True)

        # The input is associated with the label.
        toggle_input = editor_body.locator("input[type='checkbox']").first

        # Ensure it is checked to see children
        if not toggle_input.is_checked():
            toggle_label.click()

        # Verify children are visible
        # "Exclude Standard Directories"
        # "External Storage Encapsulation Name"

        expect(editor_body.get_by_text("Exclude Standard Directories")).to_be_visible()
        expect(editor_body.get_by_text("External Storage Encapsulation Name")).to_be_visible()

        # Take screenshot
        page.screenshot(path="/app/verification/external_storage_editor.png")

        browser.close()

if __name__ == "__main__":
    verify_external_storage_settings()
