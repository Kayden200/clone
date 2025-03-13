import time
import json
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_facebook_cookies():
    email = input("Enter your Facebook email: ")
    password = input("Enter your Facebook password: ")

    # Launch Chrome with undetected settings
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = uc.Chrome(options=options)
    driver.get("https://www.facebook.com/")

    # Find input fields and submit login credentials
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password, Keys.RETURN)

    time.sleep(5)  # Wait for login to complete

    # Get cookies after login
    cookies = driver.get_cookies()
    driver.quit()

    # Convert cookies to a format usable in requests
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    cookie_string = "; ".join([f"{key}={value}" for key, value in cookie_dict.items()])

    # Save cookies to a file
    with open("fb_cookies.txt", "w") as file:
        json.dump(cookie_dict, file, indent=4)

    print(f"\n✅ Facebook Cookies Extracted:\n{cookie_string}")
    print("✅ Cookies saved to fb_cookies.txt")

    return cookie_string

# Run the function
get_facebook_cookies()
