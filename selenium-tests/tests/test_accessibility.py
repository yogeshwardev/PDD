"""
test_accessibility.py – Basic accessibility & performance checks
"""

import time
import pytest
from page_objects.home_page import HomePage


class TestAccessibility:
    """Basic web accessibility and performance validations."""

    @pytest.mark.accessibility
    def test_page_has_html_lang(self, driver, base_url):
        """TC-A-001: HTML element has a lang attribute."""
        HomePage(driver, base_url).load()
        html_el = driver.find_elements("tag name", "html")
        assert len(html_el) > 0, "No <html> element found"
        lang = html_el[0].get_attribute("lang")
        assert lang and len(lang) > 0, "HTML element missing lang attribute"

    @pytest.mark.accessibility
    def test_page_has_viewport_meta(self, driver, base_url):
        """TC-A-002: Viewport meta tag exists for mobile responsiveness."""
        HomePage(driver, base_url).load()
        meta_tags = driver.find_elements(
            "xpath", "//meta[@name='viewport']"
        )
        assert len(meta_tags) > 0, "Missing viewport meta tag"

    @pytest.mark.accessibility
    def test_page_has_title(self, driver, base_url):
        """TC-A-003: Document has a non-empty <title> tag."""
        HomePage(driver, base_url).load()
        title = driver.title
        assert title and len(title.strip()) > 0, "Page title is empty"

    @pytest.mark.accessibility
    def test_page_has_charset(self, driver, base_url):
        """TC-A-004: Charset meta tag is defined."""
        HomePage(driver, base_url).load()
        charset_metas = driver.find_elements(
            "xpath", "//meta[@charset]"
        )
        content_type_metas = driver.find_elements(
            "xpath", "//meta[contains(@content,'charset')]"
        )
        assert len(charset_metas) > 0 or len(content_type_metas) > 0, (
            "No charset meta tag found"
        )

    @pytest.mark.accessibility
    def test_no_broken_images(self, driver, base_url):
        """TC-A-005: No broken images on the page."""
        HomePage(driver, base_url).load()
        images = driver.find_elements("tag name", "img")
        broken = []
        for img in images:
            natural_width = driver.execute_script(
                "return arguments[0].naturalWidth;", img
            )
            src = img.get_attribute("src") or ""
            if natural_width == 0 and src and not src.startswith("data:"):
                broken.append(src)
        assert len(broken) == 0, f"Broken images found: {broken}"

    @pytest.mark.accessibility
    def test_page_is_not_empty(self, driver, base_url):
        """TC-A-006: Page has meaningful content rendered."""
        HomePage(driver, base_url).load()
        # React Native Web uses overflow:hidden on body, so body.text may be empty.
        # Instead, check page_source for meaningful content which is more reliable.
        src = driver.page_source
        assert len(src) > 500, (
            f"Page appears empty. Source length: {len(src)}"
        )
        # Also verify there's some recognizable app content
        has_content = any(kw in src for kw in [
            "Smart", "Admission", "College", "State", "Board", "Search", "campus"
        ])
        assert has_content, "Page has no recognizable app content"

    @pytest.mark.accessibility
    def test_text_content_readable(self, driver, base_url):
        """TC-A-007: Main content has meaningful readable text."""
        HomePage(driver, base_url).load()
        src = driver.page_source
        # Should have at least some recognizable text
        keywords = ["Smart", "Admission", "College", "State", "Board", "Search"]
        found = [kw for kw in keywords if kw in src]
        assert len(found) >= 2, (
            f"Expected meaningful text on page, found keywords: {found}"
        )

    @pytest.mark.accessibility
    def test_page_font_size_not_tiny(self, driver, base_url):
        """TC-A-008: Body text has a reasonable minimum font size."""
        HomePage(driver, base_url).load()
        font_size = driver.execute_script(
            "return window.getComputedStyle(document.body).fontSize;"
        )
        if font_size:
            size_px = float(font_size.replace("px", ""))
            assert size_px >= 10, f"Body font size too small: {font_size}"


class TestPerformance:
    """Basic page load performance checks."""

    @pytest.mark.smoke
    def test_page_loads_under_15_seconds(self, driver, base_url):
        """TC-P-001: Initial page load completes within 15 seconds."""
        start = time.time()
        HomePage(driver, base_url).load()
        elapsed = time.time() - start
        assert elapsed < 15, (
            f"Page took {elapsed:.1f}s to load (threshold: 15s)"
        )

    @pytest.mark.regression
    def test_dom_content_loaded(self, driver, base_url):
        """TC-P-002: DOM is interactive after page load."""
        HomePage(driver, base_url).load()
        ready_state = driver.execute_script("return document.readyState;")
        assert ready_state in ("interactive", "complete"), (
            f"Document not ready: {ready_state}"
        )

    @pytest.mark.regression
    def test_page_source_has_content(self, driver, base_url):
        """TC-P-003: Page source is substantial (not an error page)."""
        HomePage(driver, base_url).load()
        src = driver.page_source
        assert len(src) > 1000, (
            f"Page source too short ({len(src)} chars), may be an error page"
        )

    @pytest.mark.regression
    def test_no_http_error_in_title(self, driver, base_url):
        """TC-P-004: Page title does not contain error codes."""
        HomePage(driver, base_url).load()
        title = driver.title.lower()
        error_codes = ["404", "500", "502", "503", "error"]
        found_errors = [e for e in error_codes if e in title]
        assert len(found_errors) == 0, (
            f"Page title suggests error: '{driver.title}'"
        )
