import time
import json
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_facebook_cookies():
    email = input("Enter your Facebook email: ")
    password = input("Enter your Facebook password: ")

    # Manually set chromedriver path for Termux
    chromedriver_path = "/data/data/com.termux/files/usr/bin/chromedriver"
    service = Service(chromedriver_path)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional: Run without GUI

    driver = uc.Chrome(options=options, service=service)
    driver.get("https://www.facebook.com/")

    driver.find_element("id", "email").send_keys(email)
    driver.find_element("id", "pass").send_keys(password)
    driver.find_element("id", "pass").send_keys("\n")

    time.sleep(5)

    # Get and save cookies
    cookies = driver.get_cookies()
    driver.quit()

    with open("fb_cookies.txt", "w") as file:
        json.dump({cookie['name']: cookie['value'] for cookie in cookies}, file, indent=4)

    print("\n✅ Cookies saved to fb_cookies.txt")

get_facebook_cookies()
