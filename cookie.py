import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# ✅ Set Chromedriver path for Termux
chromedriver_path = "/data/data/com.termux/files/usr/bin/chromedriver"
service = Service(chromedriver_path)

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without GUI

# ✅ Use normal Selenium instead of undetected_chromedriver
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.facebook.com/")

email = input("Enter your Facebook email: ")
password = input("Enter your Facebook password: ")

driver.find_element("id", "email").send_keys(email)
driver.find_element("id", "pass").send_keys(password)
driver.find_element("id", "pass").send_keys("\n")

time.sleep(5)

# ✅ Get and save cookies
cookies = driver.get_cookies()
driver.quit()

with open("fb_cookies.txt", "w") as file:
    json.dump({cookie['name']: cookie['value'] for cookie in cookies}, file, indent=4)

print("\n✅ Cookies saved to fb_cookies.txt")
