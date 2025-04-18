# tests/test_smokeTest.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestSmokeTest:
    def setup_method(self, method):
        # Headless Firefox setup
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts)
        self.driver.set_window_size(944, 814)
        # Explicit wait
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def test_adminPage(self):
        self.driver.get("http://127.0.0.1:5501/teton/1.6/admin.html")

        # Wait for username input
        try:
            self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        except TimeoutException:
            pytest.fail("Username input not found on admin.html")

        # Enter invalid credentials and click Login
        self.driver.find_element(By.NAME, "username").send_keys("wronguser")
        self.driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        self.driver.find_element(
            By.XPATH, "//input[@type='button' and @value='Login']"
        ).click()

        # Verify error message appears
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "errorMessage"))
            )
        except TimeoutException:
            pytest.fail("Error message not shown after failed login")

        msg = self.driver.find_element(By.CLASS_NAME, "errorMessage").text
        assert "Invalid username and password." in msg

    def test_directoryPage(self):
        self.driver.get("http://127.0.0.1:5501/teton/1.6/directory.html")

        # GRID view
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "directory-data"))
            )
        except TimeoutException:
            pytest.fail("Directory cards container not visible")
        grid_text = self.driver.find_element(By.ID, "directory-data").text
        assert "Teton Turf and Tree" in grid_text

        # LIST view
        self.driver.find_element(By.ID, "directory-list").click()
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "directory-data"))
            )
        except TimeoutException:
            pytest.fail("Directory list container not visible")
        list_text = self.driver.find_element(By.ID, "directory-data").text
        assert "Teton Turf and Tree" in list_text

    def test_homePage(self):
        self.driver.get("http://127.0.0.1:5501/teton/1.6/index.html")

        # Logo and headings
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".header-logo img"))
            )
        except TimeoutException:
            pytest.fail("Site logo not found on home page")

        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title>h1").text == "Teton Idaho"
        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title>h2").text == "Chamber of Commerce"
        assert self.driver.title == "Teton Idaho CoC"

        # Spotlights and join button
        assert self.driver.find_elements(By.CSS_SELECTOR, ".spotlight1")
        assert self.driver.find_elements(By.CSS_SELECTOR, ".spotlight2")
        assert self.driver.find_elements(By.LINK_TEXT, "Join Us")
        assert self.driver.find_elements(By.CSS_SELECTOR, "a.a-button")

    def test_joinPage(self):
        self.driver.get("http://127.0.0.1:5501/teton/1.6/join.html")

        # PAGE 1: Personal Info
        try:
            self.wait.until(EC.visibility_of_element_located((By.NAME, "fname")))
        except TimeoutException:
            pytest.fail("First-name input (fname) not found on join.html")
        self.driver.find_element(By.NAME, "fname").send_keys("John")
        self.driver.find_element(By.NAME, "lname").send_keys("Doe")
        self.driver.find_element(By.NAME, "bizname").send_keys("Teton Turf and Tree")
        self.driver.find_element(By.NAME, "biztitle").send_keys("Owner")
        self.driver.find_element(
            By.XPATH, "//input[@type='submit' and @value='Next Step']"
        ).click()

        # PAGE 2: Contact Info
        try:
            self.wait.until(EC.visibility_of_element_located((By.NAME, "email")))
        except TimeoutException:
            pytest.fail("Email input not found on join-step2.html")
        self.driver.find_element(By.NAME, "email").send_keys("john.doe@example.com")
        self.driver.find_element(By.NAME, "cellphone").send_keys("208-458-4000")
        self.driver.find_element(
            By.XPATH, "//input[@type='submit' and @value='Next Step']"
        ).click()

        # PAGE 3: Admin Login
        try:
            self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        except TimeoutException:
            pytest.fail("Username input not found on join-step3.html")
        self.driver.find_element(By.NAME, "username").send_keys("wronguser")
        self.driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        self.driver.find_element(
            By.XPATH, "//input[@type='button' and @value='Login']"
        ).click()

        # Verify error
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "errorMessage"))
            )
        except TimeoutException:
            pytest.fail("Error message not shown after join/login step")
        error = self.driver.find_element(By.CLASS_NAME, "errorMessage").text
        assert "Invalid username and password." in error
