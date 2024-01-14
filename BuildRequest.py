import json
import random
import time
import requests
import urllib3
import Config

urllib3.disable_warnings()


def check_method(url):
    method_mapping = {
        "https://www.instagram.com/accounts/emailsignup/": "GET",
        "https://www.instagram.com/api/v1/web/login_page/": "GET",
        "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/": "POST",
        'https://www.instagram.com/api/v1/accounts/check_confirmation_code/': "POST",
        "https://email-fake.com/": "GET",
        "https://www.instagram.com/api/v1/accounts/send_verify_email/": "POST",
        "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/": "POST",
    }

    return method_mapping.get(url, None)


class BuildRequest:
    def __init__(self, config: Config, url: str, data: dict = None):
        self.url = url
        self.config = config
        self.data = data
        self.method = config.method or check_method(self.url)
        self.private_requests = {}
        self.response = None
        self.build_request_handler()

    def build_request_handler(self):
        if "fake" in self.url:
            self.fake_reqeust()
        elif "accounts/emailsignup/" in self.url:
            self.email_signup_request()
        elif "login_page" in self.url:
            self.login_page_request()
        elif self.method == "POST":
            self.post_request()
        else:
            self.get_request()

    def post_request(self):
        content_len = len(json.dumps(self.data).encode('utf-8')) if self.data else 0

        headers = {
            'Host': 'www.instagram.com',
            'Content-Length': f"{content_len}",
            "Sec-Ch-Ua": self.config.user_agent["Sec-Ch-Ua"],
            'X-Ig-Www-Claim': '0',
            'Sec-Ch-Ua-Platform-Version': '6.5.0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Web-Device-Id': self.config.info["Cookies"]['ig_did'],
            'Dpr': '1',
            "Sec-Ch-Ua-Full-Version-List": self.config.user_agent["Sec-Ch-Ua-Full-Version-List"],
            'X-Csrftoken': self.config.info["Cookies"]['csrftoken'],
            'Sec-Ch-Ua-Model': '\"\"',
            "Sec-Ch-Ua-Platform": self.config.user_agent["Sec-Ch-Ua-Platform"],
            'X-Ig-App-Id': '936619743392459',
            'Sec-Ch-Prefers-Color-Scheme': 'light',
            'Sec-Ch-Ua-Mobile': '?0',
            'X-Instagram-Ajax': f'{self.config.x_instagram_ajax}',
            'User-Agent': self.config.user_agent["User-Agent"],
            'Viewport-Width': '1153',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'X-Asbd-Id': '129477',
            'Origin': 'https://www.instagram.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.instagram.com/accounts/emailsignup/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en;q=0.9',
        }

        headers.update(self.config.user_agent)

        self.private_requests = {
            "method": self.method,
            "url": self.url,
            "cookies": self.config.info["Cookies"],
            "headers": headers,
            "data": self.data,
            "proxy": self.config.proxy,
        }

    def get_request(self):
        headers = {
            "Host": "www.instagram.com",
            "Sec-Ch-Ua": self.config.user_agent["Sec-Ch-Ua"],
            "X-Ig-Www-Claim": "0",
            "Sec-Ch-Ua-Platform-Version": "6.5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Dpr": "1",
            "Sec-Ch-Ua-Full-Version-List": self.config.user_agent["Sec-Ch-Ua-Full-Version-List"],
            "Sec-Ch-Prefers-Color-Scheme": "light",
            "Sec-Ch-Ua-Platform": self.config.user_agent["Sec-Ch-Ua-Platform"],
            "X-Ig-App-Id": "936619743392459",
            "Sec-Ch-Ua-Model": "\"\"",
            "Sec-Ch-Ua-Mobile": "?0",
            'User-Agent': self.config.user_agent["User-Agent"],
            "Viewport-Width": "1153",
            "Accept": "*/*",
            "X-Asbd-Id": "129477",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.instagram.com/accounts/emailsignup/",
            "Accept-Encoding": "gzip, deflate, br",
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        headers.update(self.config.user_agent)

        self.private_requests = {
            "method": self.method,
            "url": self.url,
            "cookies": self.config.info["Cookies"],
            "headers": headers,
            "proxy": self.config.proxy,
        }

    def fake_reqeust(self):
        headers = {
            'Host': 'email-fake.com',
            'User-Agent': self.config.user_agent["User-Agent"],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            "Cookie": f"surl={self.config.fake_cookies}",
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': "no-cache",
            'Cache-Control': 'no-cache'
        }

        self.private_requests = {
            "method": self.method,
            "url": self.url,
            "cookies": "",
            "headers": headers,
            "proxy": self.config.proxy,
        }

    def email_signup_request(self):
        headers = {
            "Sec-Ch-Ua": self.config.user_agent["Sec-Ch-Ua"],
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": self.config.user_agent["Sec-Ch-Ua-Platform"],
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.config.user_agent["User-Agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }
        self.private_requests = {
            "method": self.method,
            "url": self.url,
            "cookies": "",
            "headers": headers,
            "proxy": self.config.proxy,
        }

    def login_page_request(self):
        headers = {
            "Host": "www.instagram.com",
            "Sec-Ch-Ua": self.config.user_agent["Sec-Ch-Ua"],
            "X-Ig-Www-Claim": "0",
            "Sec-Ch-Ua-Platform-Version": "6.5.0",
            "X-Requested-With": "XMLHttpRequest",
            "X-Web-Device-Id": self.config.info["PreLogin"]["_js_ig_did"],
            "Dpr": "1",
            "Sec-Ch-Ua-Full-Version-List": self.config.user_agent["Sec-Ch-Ua-Full-Version-List"],
            "Sec-Ch-Prefers-Color-Scheme": "light",
            "X-Csrftoken": self.config.info["PreLogin"]["csrftoken"],
            "Sec-Ch-Ua-Platform": self.config.user_agent["Sec-Ch-Ua-Platform"],
            "X-Ig-App-Id": "936619743392459",
            "Sec-Ch-Ua-Model": "\"\"",
            "Sec-Ch-Ua-Mobile": "?0",
            'User-Agent': self.config.user_agent["User-Agent"],
            "Viewport-Width": "1153",
            "Accept": "*/*",
            "X-Asbd-Id": "129477",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.instagram.com/accounts/emailsignup/",
            "Accept-Encoding": "gzip, deflate, br",
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        headers.update(self.config.user_agent)
        # cookie_dict = self.config.info["PreLogin"]
        cookie_dict = {"_js_ig_did": self.config.info["PreLogin"]["_js_ig_did"],
                       "_js_datr": self.config.info["PreLogin"]["_js_datr"]}

        self.private_requests = {
            "method": self.method,
            "url": self.url,
            "cookies": cookie_dict,
            "headers": headers,
            "proxy": self.config.proxy,
        }

    def send(self) -> requests:
        time.sleep(random.uniform(10, 30))
        packet = self.private_requests
        timeout_request = 60
        if self.config.proxy_inactive:
            packet["proxy"] = None
        retries = 0
        while retries <= 10:
            retries += 1
            try:
                if packet["method"] == "POST":
                    self.response = requests.post(url=packet["url"], headers=packet["headers"],
                                                  cookies=packet["cookies"], data=packet["data"],
                                                  proxies=packet["proxy"], verify=False, timeout=timeout_request)
                elif packet["method"] == "GET":
                    self.response = requests.get(url=packet["url"], headers=packet["headers"],
                                                 cookies=packet["cookies"],
                                                 proxies=packet["proxy"], verify=False,
                                                 timeout=timeout_request)
                return True
            except requests.RequestException as e:
                print(f"[-] ERROR: BuildRequest.send(): url: {self.url}")
                print(f"[-] ERROR: BuildRequest.send(): Request error: {e}")
                time.sleep(10)
                continue
            except Exception as e:
                print(f"[-] ERROR: BuildRequest.send(): Request error: {e}")
                continue
            finally:
                self.config.proxy_inactive = False
        return False

