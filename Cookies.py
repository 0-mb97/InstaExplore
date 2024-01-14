import json
from pathlib import Path
import BuildRequest
import Config


def cookie_to_dict(cookie_values):
    cookies = {}
    for cookie in cookie_values:
        parts = cookie.split(";")[0]
        if '=' in parts:
            key, value = parts.split("=")
            cookies[key.strip()] = value.strip()
    return cookies


class Cookies:
    _cookies = None  # Define _cookies in the class body

    def __init__(self, config: Config, new: bool = True, username: str = "last", csrftoken=None, datr=None, mid=None,
                 ig_nrcb="1", ig_did=None):
        self.url = "https://www.instagram.com/api/v1/web/login_page/"
        self.config = config
        self.cookie_file = ""
        self.cookie_path = f"create_account/cookies/{username}.json"

        self.csrftoken = csrftoken if csrftoken else config.info["PreLogin"]["csrftoken"]
        self.js_datr = datr if datr else config.info["PreLogin"]["_js_datr"]
        self.js_ig_did = ig_did if ig_did else config.info["PreLogin"]["_js_ig_did"]
        self.mid = mid
        self.ig_nrcb = ig_nrcb
        self.cookie_handler(load=new)

    @property
    def cookies(self) -> dict:
        return self._cookies

    @cookies.setter
    def cookies(self, value):
        # Add any additional validation or processing logic here if needed
        self._cookies = value

    def update_cookie_path(self, username: str):
        self.cookie_path = f"create_account/cookies/{username}"

    def get_cookies(self, username: str = None):
        if username:
            self.update_cookie_path(username)

        if Path.exists(Path(self.cookie_path)):
            with open(self.cookie_path, "r") as f:
                self._cookies = json.load(f)
            print("[+] INFO: Cookies.get_cookies(). Done.")
        else:
            self.set_cookies()

    def set_cookies(self):
        self.config.cookies = None
        login_result = self.login_page()
        if login_result.status_code == 200:
            all_headers = login_result.headers.items()
            headers_dict = dict(all_headers)
            set_cookie_header = headers_dict.get("Set-Cookie", "")
            set_cookie_values = set_cookie_header.split(", ")
            self._cookies = self.arrange_cookies_values(set_cookie_values)
            print("[+] INFO: Cookies.set_cookies(): Done. ")
            self.to_string()
            return True
        else:
            print("[-] ERROR: Cookies.set_cookies(): Account Not Found")
            return None

    def login_page(self):

        br = BuildRequest.BuildRequest(config=self.config, url=self.url)
        br.send()
        if br.response:
            return br.response
        else:
            raise Exception("[-] ERROR: Cookies.login_page(): Exception : login_page response is None")

    def to_string(self):
        try:
            with open(self.cookie_path, "w") as f:
                f.write(json.dumps(self._cookies) + "\n")
            print("[+] INFO: Cookies.to_string(): Done.")
        except Exception as e:
            print(f"[-] ERROR: Cookies.to_string() : false.\ngot exception: {e}")

    def run(self):
        self.cookie_handler()

    def cookie_handler(self, load: bool = True):
        try:
            if not load:
                self.get_cookies()
            else:
                self.set_cookies()
            print("Cookies: ", self._cookies)
            if self._cookies["mid"] is None:
                print("[-] ERROR : Cookies.cookies_handler(): didnt get mid value")
                raise Exception("didnt get mid value")
            else:
                self.config.info["Cookies"] = self._cookies
        except Exception as e:
            print(f"[-] ERROR Cookies.cookie_handler(): got exception: {e} ")
            raise Exception

    def arrange_cookies_values(self, mess) -> dict:
        for header in mess:
            if "mid" in header:
                if "=" in header:
                    key, value = header.split(";")[0].split("=")
                    self.mid = value.strip()
                    break
        fix = {
            "ig_did": self.js_ig_did,
            "datr": self.js_datr,
            "csrftoken": self.csrftoken,
            "ig_ncrb": self.ig_nrcb,
            "mid": self.mid
        }
        return fix
