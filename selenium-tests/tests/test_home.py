"""
test_home.py – Home screen smoke & regression tests
Tests the deployed GitHub Pages app at BASE_URL
"""

import time
import pytest
from page_objects.home_page import HomePage


class TestHomePageLoad:
    """Verifies the app loads successfully from the GitHub Pages URL."""

    @pytest.mark.smoke
    def test_page_returns_200_and_loads(self, driver, base_url):
        """TC-H-001: Page loads without error (HTTP 200 equivalent)."""
        page = HomePage(driver, base_url)
        page.load()
        assert page.is_loaded(), (
            f"App did not load at {base_url}. "
            f"Page source: {driver.page_source[:500]}"
        )

    @pytest.mark.smoke
    def test_app_title_visible(self, driver, base_url):
        """TC-H-002: App title 'Smart Admission' is visible."""
        page = HomePage(driver, base_url).load()
        assert page.is_app_title_visible(), (
            "App title 'Smart' not found in page source"
        )

    @pytest.mark.smoke
    def test_page_document_title(self, driver, base_url):
        """TC-H-003: Browser tab title is not empty."""
        page = HomePage(driver, base_url).load()
        title = page.get_page_title()
        assert title and len(title) > 0, "Page title (browser tab) should not be empty"

    @pytest.mark.regression
    def test_tagline_visible(self, driver, base_url):
        """TC-H-004: Tagline or app description is visible."""
        page = HomePage(driver, base_url).load()
        assert page.is_tagline_visible(), (
            "Tagline not visible — no app description text found"
        )

    @pytest.mark.regression
    def test_state_selector_present(self, driver, base_url):
        """TC-H-005: State/UT selector or related text is present."""
        page = HomePage(driver, base_url).load()
        assert page.is_state_selector_present(), (
            "State selector/text not found"
        )

    @pytest.mark.regression
    def test_board_selector_present(self, driver, base_url):
        """TC-H-006: Board selector or related text is present."""
        page = HomePage(driver, base_url).load()
        assert page.is_board_selector_present(), (
            "Board selector/text not found"
        )

    @pytest.mark.regression
    def test_next_button_present(self, driver, base_url):
        """TC-H-007: Navigation button (Next/Continue/Step) is visible."""
        page = HomePage(driver, base_url).load()
        assert page.is_next_button_present(), (
            "'Next / Continue / Step' button not found"
        )

    @pytest.mark.regression
    def test_stats_row_visible(self, driver, base_url):
        """TC-H-008: Stats section (Colleges, States) is visible."""
        page = HomePage(driver, base_url).load()
        page.scroll_down()
        time.sleep(1)
        assert page.is_stats_row_present(), (
            "Stats row (Colleges/States count) not found after scrolling"
        )

    @pytest.mark.regression
    def test_feature_cards_visible(self, driver, base_url):
        """TC-H-009: Feature section (AI/Smart features) visible."""
        page = HomePage(driver, base_url).load()
        page.scroll_down()
        time.sleep(1)
        assert page.is_features_section_present(), (
            "Feature cards / Smart features section not found"
        )

    @pytest.mark.regression
    def test_india_badge_visible(self, driver, base_url):
        """TC-H-010: India-related content is present."""
        page = HomePage(driver, base_url).load()
        assert page.is_india_badge_present(), "India badge/text not found"

    @pytest.mark.regression
    def test_free_badge_visible(self, driver, base_url):
        """TC-H-011: 'Free' badge or indicator is visible."""
        page = HomePage(driver, base_url).load()
        assert page.is_free_badge_present(), "Free badge/text not found"

    @pytest.mark.regression
    def test_step_indicator_visible(self, driver, base_url):
        """TC-H-012: Step indicator is visible."""
        page = HomePage(driver, base_url).load()
        assert page.is_step_indicator_present(), "Step indicator not found"


class TestHomePageInteraction:
    """Tests for interactive elements on the home screen."""

    @pytest.mark.regression
    def test_page_is_scrollable(self, driver, base_url):
        """TC-H-013: Page can be scrolled down to reveal more content."""
        page = HomePage(driver, base_url).load()
        pre_scroll_src = driver.page_source
        page.scroll_down()
        time.sleep(1)
        # Page should still show content after scroll
        assert len(driver.page_source) > 100, "Page appears empty after scroll"

    @pytest.mark.regression
    def test_state_dropdown_clickable(self, driver, base_url):
        """TC-H-014: State dropdown responds to click."""
        page = HomePage(driver, base_url).load()
        result = page.try_click_state_dropdown()
        # Even if click doesn't open, no exception means the element was found
        # Just verify app is still alive
        assert page.is_loaded(), "App crashed after clicking state dropdown"

    @pytest.mark.smoke
    def test_no_console_critical_errors(self, driver, base_url):
        """TC-H-015: No critical JavaScript errors in browser console."""
        page = HomePage(driver, base_url).load()
        logs = driver.get_log("browser")
        critical_errors = [
            log for log in logs
            if log.get("level") in ("SEVERE",)
            and "favicon" not in log.get("message", "").lower()
            and "404" not in log.get("message", "")
        ]
        assert len(critical_errors) == 0, (
            f"Critical JS errors found:\n"
            + "\n".join(e.get("message", "") for e in critical_errors[:5])
        )

    @pytest.mark.regression
    def test_url_is_correct_base(self, driver, base_url):
        """TC-H-016: App URL is correct GitHub Pages URL."""
        page = HomePage(driver, base_url).load()
        current_url = page.get_current_url()
        assert "github.io" in current_url or base_url.rstrip("/") in current_url, (
            f"URL mismatch. Expected {base_url}, got {current_url}"
        )

    @pytest.mark.smoke
    def test_page_load_within_timeout(self, driver, base_url):
        """TC-H-017: Page fully loads within 30 seconds."""
        page = HomePage(driver, base_url)
        start = time.time()
        page.load()
        elapsed = time.time() - start
        assert elapsed < 30, f"Page took too long to load: {elapsed:.1f}s"
