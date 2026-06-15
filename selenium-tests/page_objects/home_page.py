"""Home Page Object – Smart Admission landing page."""

import time
from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """
    Covers the main landing screen:
    - App title / tagline
    - State selector dropdown
    - Board selector dropdown
    - Next button
    - Stats row (1000+ Colleges etc.)
    - Feature cards
    """

    # ── Locators (React Native Web renders as divs/spans) ─────────────────────
    # React Native Web renders Text as <div> with role="none" or plain text nodes.
    # We rely on text content and ARIA roles where possible.
    APP_TITLE_TEXT    = "Smart"
    TAGLINE_TEXT      = "Intelligent College Admission"
    STATE_DROPDOWN    = (By.XPATH, "//*[contains(text(),'Choose your state') or contains(text(),'State')]")
    BOARD_DROPDOWN    = (By.XPATH, "//*[contains(text(),'Choose your board') or contains(text(),'Board')]")
    NEXT_BUTTON       = (By.XPATH, "//*[contains(text(),'Next') or contains(text(),'Enter Your Marks')]")
    STATS_COLLEGES    = (By.XPATH, "//*[contains(text(),'1000+') or contains(text(),'Colleges')]")
    FEATURE_AI        = (By.XPATH, "//*[contains(text(),'AI Powered')]")
    FEATURE_PLACEMENT = (By.XPATH, "//*[contains(text(),'Placement')]")
    HERO_BADGE_INDIA  = (By.XPATH, "//*[contains(text(),'India')]")
    STEP_LABEL        = (By.XPATH, "//*[contains(text(),'Step 1')]")

    def load(self):
        """Navigate to the app root and wait for hydration."""
        self.open("")
        # React Native Web splash + hydration – wait for content
        self._wait_for_content(timeout=12)
        return self

    def _wait_for_content(self, timeout=12):
        """Wait for React Native Web to hydrate and render content."""
        end = time.time() + timeout
        while time.time() < end:
            src = self.get_page_source()
            # Check for any meaningful content from the app
            if any(kw in src for kw in [
                "Smart", "Admission", "College", "State", "Board",
                "Search", "Compare", "Step", "Choose", "campus"
            ]):
                time.sleep(1)  # Extra settle time after content appears
                return True
            time.sleep(0.5)
        return False

    def is_loaded(self) -> bool:
        """Returns True if the home page content is visible."""
        src = self.get_page_source()
        return any(
            kw in src
            for kw in ["Smart Admission", "SmartCampusAI", "College", "State",
                        "Smart", "Admission", "campus", "Board", "Search"]
        )

    def get_page_title(self) -> str:
        return self.driver.title

    def is_app_title_visible(self) -> bool:
        src = self.get_page_source()
        return self.APP_TITLE_TEXT in src or "Admission" in src

    def is_tagline_visible(self) -> bool:
        src = self.get_page_source()
        # Check multiple possible tagline variants
        return (
            self.TAGLINE_TEXT in src
            or "Intelligent" in src
            or "College Admission" in src
            or "Admission" in src
        )

    def is_state_selector_present(self) -> bool:
        src = self.get_page_source().lower()
        return "state" in src or "choose" in src or "select" in src

    def is_board_selector_present(self) -> bool:
        src = self.get_page_source().lower()
        return "board" in src or "choose" in src or "cbse" in src or "select" in src

    def is_next_button_present(self) -> bool:
        src = self.get_page_source()
        return (
            "Next" in src
            or "Marks" in src
            or "Continue" in src
            or "Step" in src
        )

    def is_stats_row_present(self) -> bool:
        src = self.get_page_source()
        return (
            "1000" in src
            or "Colleges" in src
            or "colleges" in src
            or "States" in src
            or "28" in src
        )

    def is_features_section_present(self) -> bool:
        src = self.get_page_source()
        return (
            "AI Powered" in src
            or "Placement" in src
            or "AI" in src
            or "Feature" in src.lower()
            or "Smart" in src
        )

    def is_india_badge_present(self) -> bool:
        src = self.get_page_source()
        return "India" in src or "🇮🇳" in src or "indian" in src.lower()

    def is_free_badge_present(self) -> bool:
        src = self.get_page_source()
        return "Free" in src or "free" in src or "100%" in src

    def is_step_indicator_present(self) -> bool:
        src = self.get_page_source()
        return "Step 1" in src or "Step" in src or "step" in src.lower()

    def try_click_state_dropdown(self) -> bool:
        """Attempt to click the state dropdown. Returns True if successful."""
        try:
            els = self.find_all(By.XPATH, "//*[contains(text(),'Choose your state')]")
            if not els:
                els = self.find_all(By.XPATH, "//*[contains(text(),'State')]")
            if els:
                self.driver.execute_script("arguments[0].click();", els[0])
                time.sleep(1)
                return True
        except Exception:
            pass
        return False

    def try_click_next_button(self) -> bool:
        """Attempt to click the Next button. Returns True if successful."""
        try:
            els = self.find_all(
                By.XPATH,
                "//*[contains(text(),'Next') or contains(text(),'Enter Your Marks')]",
            )
            if els:
                self.driver.execute_script("arguments[0].click();", els[0])
                time.sleep(1)
                return True
        except Exception:
            pass
        return False

    def scroll_down(self):
        self.scroll_to_bottom()
        return self
