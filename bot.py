import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

EMAIL = os.environ["LINKEDIN_EMAIL"]
PASSWORD = os.environ["LINKEDIN_PASSWORD"]

POST_TEXT = "🚀 My automated LinkedIn post from GitHub Actions!"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Login
driver.get("https://www.linkedin.com/login")
time.sleep(3)

driver.find_element(By.ID, "username").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

time.sleep(5)

# Go to feed
driver.get("https://www.linkedin.com/feed/")
time.sleep(5)

# Click start post
driver.find_element(By.XPATH, "//button[contains(@class,'share-box-feed-entry__trigger')]").click()
time.sleep(3)

# Enter content
driver.find_element(By.XPATH, "//div[@role='textbox']").send_keys(POST_TEXT)
time.sleep(2)

# Click post
driver.find_element(By.XPATH, "//button[contains(@class,'share-actions__primary-action')]").click()

time.sleep(5)

driver.quit()
