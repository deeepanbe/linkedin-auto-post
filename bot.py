from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

# Initialize Chrome driver with headless mode for CI/CD
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create driver instance BEFORE using it
driver = webdriver.Chrome(options=chrome_options)

# Get LinkedIn credentials from environment variables
email = os.getenv('LINKEDIN_EMAIL')
password = os.getenv('LINKEDIN_PASSWORD')

try:
    # Navigate to LinkedIn
    driver.get('https://www.linkedin.com/login')
    
    # Login
    driver.find_element(By.ID, 'username').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    
    time.sleep(3)
    
    # Wait for post button and click
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Start a post")]')))
    button.click()
    
    # Post content
    post_textarea = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
    post_textarea.send_keys("Your post content here!")
    
    # Click post button
    another_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Post")]')))
    another_button.click()
    
    print("Post published successfully!")
    
finally:
    # Always close the driver
    driver.quit()