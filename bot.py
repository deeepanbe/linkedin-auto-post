import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

print("🚀 Starting LinkedIn Bot...")

EMAIL = os.environ.get("LINKEDIN_EMAIL")
PASSWORD = os.environ.get("LINKEDIN_PASSWORD")

POST_TEXT = "🚀 My automated LinkedIn post from GitHub Actions!"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = None

try:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    print("🌐 Opening LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(5)

    print("🔐 Entering credentials...")
    driver.find_element(By.ID, "username").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(8)

    print("🏠 Opening feed...")
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(8)

    print("✍️ Clicking start post...")
    driver.find_element(By.XPATH, "//button[contains(@class,'share-box-feed-entry__trigger')]").click()
    time.sleep(5)

    print("📝 Writing post...")
    driver.find_element(By.XPATH, "//div[@role='textbox']").send_keys(POST_TEXT)
    time.sleep(3)

    print("🚀 Clicking post button...")
    driver.find_element(By.XPATH, "//button[contains(@class,'share-actions__primary-action')]").click()

    print("✅ Post submitted!")

    time.sleep(5)

except Exception as e:
    print("❌ ERROR OCCURRED:")
    print(str(e))

    if driver:
        driver.save_screenshot("error.png")

    raise

finally:
    if driver:
        driver.quit()

print("🎉 Bot finished")
