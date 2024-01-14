import random
import re
import time
from pathlib import Path
import urllib3
from bs4 import BeautifulSoup
import BuildRequest
import requests
from Config import Config
from timeout_decorator import timeout

urllib3.disable_warnings()


@timeout(60)
def send(br: BuildRequest) -> requests:
    time.sleep(random.randrange(8, 10))
    packet = br.private_requests
    while True:
        try:
            # print(packet["method"])
            if packet["method"] == "POST":
                response = requests.post(url=packet["url"], headers=packet["headers"], cookies=packet["cookies"],
                                         data=packet["data"],
                                         proxies=packet["proxy"], verify=False)
            elif packet["method"] == "GET":
                response = requests.get(url=packet["url"], headers=packet["headers"], cookies=packet["cookies"],
                                        proxies=packet["proxy"], verify=False,
                                        )
            else:
                return None
            return response

        except requests.RequestException as e:
            print(f"Request error: send(). {e}")
            time.sleep(6)
            continue


def check_path(path: str):
    dir_path = Path(f"{path.split('/')[:-1]}")
    if not Path.exists(Path(dir_path)):
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            print("[-] File Name not exist.PreLogin(set()) ")
            return False
    if not Path(path).exists():
        with open(path, "r") as f:
            pass


def extract_ig_instagram_ajax():
    with open("html", "r") as f:
        html_content = f.read()
    match = re.search(r'data-btmanifest="(\d+)_main"', html_content)

    if match:
        data_btmanifest_value = match.group(1)
        return data_btmanifest_value
    else:
        print("Unable to extract the value.")


def extract_code_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    subj_divs = soup.find_all('div', class_='fem subj_div_45g45gg')
    time_divs = soup.find_all('div', class_='fem time_div_45g45gg')

    if subj_divs:
        # Extract the text content of the last element
        last_subject = subj_divs[0].text.strip()

        # Extract the number from the subject (assuming it's always at the beginning)
        last_number = ''.join(c for c in last_subject if c.isdigit())
        # print("Last number: ", last_number)
        if time_divs:
            last_time = time_divs[0].text.strip()
        print(f"last number: {last_number} : last_time : {last_time}")
        return last_number, last_time

    else:
        print("Element not found in HTML.")
        return None


def print_user_login(user: dict):
    return f"{user['username']}:{user['password']}:{user['first_name']}:{user['email'][0]}"


def extract_signup_code(payload):
    return str(payload).split(",")[0].split(":")[1].strip("\"")


def get_username_payload(conf: Config):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': f'csrftoken={conf.info["PreLogin"]["csrftoken"]}; ig_did={conf.info["PreLogin"]["_js_ig_did"]}',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    return headers


def check_username_in_title(username, conf: Config):
    payload = get_username_payload(conf=conf)
    url = f'https://www.instagram.com/{username}/'
    # Perform login request
    response = requests.post(url, headers=payload, proxies=conf.proxy)

    if response.status_code == 200:
        # If login is successful, check if the name is in the title tag
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.title.text.lower()

        # if name.lower() in title_tag:
        if username.lower() in title_tag:
            return True
        else:
            return False
    else:
        print(
            f"CheckCredential.check_username_in_title(): cant get status_code 200: the last is {response.status_code}")
        return None


def generate_new_fake_mail(proxy: dict):
    url = 'https://email-fake.com/'
    p = proxy
    while True:
        for j in range(2):
            for i in range(2):
                try:
                    req = requests.get(url, proxies=p, verify=False, timeout=15)
                    soup = BeautifulSoup(req.content, "html.parser")
                    mail = soup.find_all("span", {"id": "email_ch_text"})
                    return mail[0].text
                except (requests.RequestException, TimeoutError) as e:
                    print(f"Request error: CreateAccountFunctions().generate_new_fake_mail(). maybe timeout:  {e}")
                    time.sleep(4)
                    continue
                except OSError as e:
                    print(f"[-] ERROR CreateAccountFunctions().generate_new_fake_mail(). : {e}")
                    time.sleep(4)
                    continue
            print(f"[-] Warning: CreateAccountFunctions.generate_new_fake_mail(): Setting proxy to None... Retrying.")
            p = None
        print(f"[-] Warning: CreateAccountFunctions().generate_new_fake_mail(): Sleeping for 40 secs... Retrying")
        time.sleep(40)


def file_to_account(line: str):
    return line.strip("\n").split(":")


def cookie_to_dict(cookie_values):
    cookies = {}
    for cookie in cookie_values:
        parts = cookie.split(";")[0]
        if '=' in parts:
            key, value = parts.split("=")
            cookies[key.strip()] = value.strip()
    return cookies
