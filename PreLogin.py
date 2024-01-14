import json
import re
from pathlib import Path
from CreateAccountFunctions import extract_ig_instagram_ajax
import BuildRequest
import Config


class PreLogin:

    def __init__(self, config: Config, filename: str = "last", new: bool = True, js_ig_did=None, js_datr=None,
                 csrftoken=None, x_instagram_ajax=None):
        self.x_instagram_ajax = x_instagram_ajax
        self.filename = f"create_account/pre_login/{filename}.json"
        self.config = config
        self.js_ig_did = js_ig_did
        self.js_datr = js_datr
        self.csrftoken = csrftoken

        self.response = None

        self.PreLogin_handler(new=new)

    def email_signup(self):
        url = "https://www.instagram.com/accounts/emailsignup/"

        br = BuildRequest.BuildRequest(config=self.config, url=url)
        br.send()
        if br.response:
            self.response = br.response
        else:
            raise Exception("Exception: email_signup response is None")
        return True

    def set_to_file(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps({"js_ig_did": self.js_ig_did, "js_datr": self.js_datr, "csrftoken": self.csrftoken,
                                "x_instagram_ajax": self.x_instagram_ajax}))
            print("[+] PreLogin saved successfully. to file")
        return True

    def read_from_file(self):

        if Path.exists(Path(f"{self.filename}")):
            with open(self.filename, 'r') as f:
                info = json.load(f)

            self.js_ig_did = info["js_ig_did"]
            self.js_datr = info["js_datr"]
            self.csrftoken = info["csrftoken"]
            self.x_instagram_ajax = info["x_instagram_ajax"]

            print("[+] PreLogin loaded successfully. from file")
            return True
        else:
            print("[-] File Name not exist")
            return False

    def extract_js_value(self):

        html_data = self.response.text
        with open("html", "w") as f:
            f.write(html_data)
        if self.x_instagram_ajax is None:
            self.x_instagram_ajax = extract_ig_instagram_ajax()

        js_datr_match = re.search(r'"_js_datr":\s*{"value":"(.*?)",', html_data)
        js_ig_did_match = re.search(r'"_js_ig_did":\s*{"value":"(.*?)",', html_data)

        # Extract name and value
        js_datr_name, js_datr_value = "_js_datr", js_datr_match.group(1) if js_datr_match else None
        js_ig_did_name, js_ig_did_value = "_js_ig_did", js_ig_did_match.group(1) if js_ig_did_match else None
        if self.js_datr is None:
            self.js_datr = js_datr_value
        if self.js_ig_did is None:
            self.js_ig_did = js_ig_did_value

        set_cookie_headers = self.response.headers.get("Set-Cookie")
        if self.response.status_code == 200:

            if set_cookie_headers:
                key, value = set_cookie_headers.split(";")[0].split("=")
                if key == 'csrftoken':
                    self.csrftoken = value
                return True

            else:
                print("No Set-Cookie headers found in the response.")

        else:
            print(f"Error: {self.response.status_code}")
            raise Exception

    def PreLogin_handler(self, new: bool):
        if not new:
            if self.read_from_file():
                self.update_config()
            else:
                new = True
        if new:
            if self.email_signup():
                if self.extract_js_value():
                    self.update_config()
                    self.set_to_file()
        print(self.config.info["PreLogin"], "x_instagram_ajax: ", self.config.x_instagram_ajax)

    def update_config(self):

        self.config.info["PreLogin"]["_js_ig_did"] = self.js_ig_did
        self.config.info["PreLogin"]["_js_datr"] = self.js_datr
        self.config.info["PreLogin"]["csrftoken"] = self.csrftoken
        self.config.x_instagram_ajax = self.x_instagram_ajax
