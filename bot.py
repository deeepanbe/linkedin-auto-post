import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("🚀 Starting LinkedIn Bot...")

EMAIL = os.environ.get("LINKEDIN_EMAIL")
PASSWORD = os.environ.get("LINKEDIN_PASSWORD")

POST_TEXT = "🚀 My automated LinkedIn post from GitHub Actions!"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = None

try:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 20)

    # 🔐 LOGIN
    print("🔐 Logging in...")
    driver.get("https://www.linkedin.com/login")

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # 🏠 WAIT FOR FEED LOAD
    print("🏠 Waiting for feed...")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    driver.get("https://www.linkedin.com/feed/")

    # ✍️ CLICK "START POST" BUTTON (MULTIPLE FALLBACKS)
    print("✍️ Finding post button...")

    try:
        post_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'share-box-feed-entry__trigger')]")).__trigger
        )
    except:
        try:
            post_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Start a post')]")).__start_post
            )
        except:
            post_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Start a post')]").__start_post_button__
            )

    post_button.click()

    # 📝 ENTER TEXT
    print("📝 Writing post...")
    textbox = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
    )
    textbox.send_keys(POST_TEXT)

    # 🚀 CLICK POST
    print("🚀 Posting...")
    post_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'share-actions__primary-action')]")).__post_actions__________
    )
    post_btn.click()

    print("✅ Post submitted!")

except Exception as e:
    print("❌ ERROR:", str(e))
    if driver:
        driver.save_screenshot("error.png")
    raise

finally:
    if driver:
        driver.quit()

print("🎉 Bot finished")