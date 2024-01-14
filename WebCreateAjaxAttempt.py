import json
import random
import time
from pathlib import Path
import PasswordEncrypting
import BuildRequest
import Config
import GenerateAccount as account
from CreateAccountFunctions import generate_new_fake_mail


def parse_response(response):
    response = response.json()
    username_suggestions = response.get('username_suggestions', [])

    return username_suggestions


class WebCreateAjaxAttempt:

    def __init__(self, config: Config, new: bool = True, filename: str = "last", username=None, first_name=None,
                 mail=None, password=None,
                 enc_password=None, opt_into_one_tap=False):
        self.config = config
        self.last_response = None
        self.username_list = []
        self.filename = ""
        self.update_filename(filename)

        if not new:
            new = not self.read_from_file(filename)
        if new:
            self.password = password if password else account.generatePassword()
            self.enc_password = enc_password if enc_password else PasswordEncrypting.password_encrypt(self.password)
            self.email = mail if mail else generate_new_fake_mail(self.config.proxy)
            self.username = username
            self.first_name = first_name if first_name else account.generatingName()
            self.opt_into_one_tap = opt_into_one_tap
        self.run(new)

    def create_username(self):
        if not self.username_list:
            self.username_list = parse_response(self.last_response)
        return self.get_username_from_list()

    def update_username(self, username=None):
        if username:
            self.username = username
        else:
            self.username = self.create_username()

    def update_filename(self, filename):
        self.filename = f"create_account/WebCreateAjaxAttempt/{filename}.json"

    def web_create_ajax_attempt(self, data: dict):

        url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"

        br = BuildRequest.BuildRequest(config=self.config, url=url, data=data)
        br.send()
        if br.response:
            self.last_response = br.response
        else:
            raise Exception("[-] ERROR: Exception: WebCreateAjaxAttempt.web_create_ajax_attempt() response is None")
        return True

    def ToString(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps({"password": self.password, "enc_password": self.enc_password, "email": self.email,
                                "first_name": self.first_name, "username": self.username,
                                "opt_into_one_tap": self.opt_into_one_tap, "username_list": self.username_list}))
            print("[+] INFO: WebCreateAjaxAttempt.ToString: Done.")
        return True

    def read_from_file(self, filename):
        self.update_filename(filename)
        if Path(self.filename).exists():
            try:
                with open(self.filename, 'r') as f:
                    info = json.load(f)
                self.password = info["password"]
                self.enc_password = info["enc_password"]
                self.email = info["email"]
                self.first_name = info["first_name"]
                self.username = info["username"]
                self.opt_into_one_tap = info["opt_into_one_tap"]
                self.username_list = info["username_list"]
                print(f"[+] INFO: SendVerifyEmail.read_from_file(): Done.")
                return True
            except json.JSONDecodeError as e:
                print(f"[-] ERROR: WebCreateAjaxAttempt.read_from_file(): Error decoding JSON: {e}")
                return False
            except Exception as e:
                print(f"[-] ERROR: WebCreateAjaxAttempt.read_from_file(): An unexpected error occurred: {e}")
                return False
        else:
            print("[!] Warning: WebCreateAjaxAttempt.read_from_file(): File does not exist.continue with default value")
            return False

    def get_username_from_list(self):
        if self.username_list or len(self.username_list) >= 1:
            user = self.username_list[0]
            self.username_list = self.username_list[1:]
            self.username_list = self.username_list
            self.ToString()
            return user
        else:
            return f"akdurncs{random.randint(100, 1000000)}"

    def handle_response(self):
        try:
            if self.last_response.status_code == 200:
                try:
                    result = json.loads(self.last_response.text)["dryrun_passed"]
                    if result is True:
                        print(f"[+] INFO: WebCreateAjaxAttempt.handle_response: dryrun_passed : Done.")
                except KeyError:
                    print("dryrun_passed: ", json.loads(self.last_response.text)["status"])
                except Exception as e:
                    print(
                        f"[-] ERROR: WebCreateAjaxAttempt.handle_response() : Got status code 200 with unknown response {self.last_response.text}")
                    print(f"[-] ERROR: WebCreateAjaxAttempt.handle_response() : Got error type {e}")
                finally:
                    return True

            elif self.last_response.status_code == 429:
                try:
                    result = json.loads(self.last_response.text)["error_type"]
                    if result == 'rate_limit_error':
                        print(
                            f"[-] ERROR: WebCreateAjaxAttempt.handle_request() : Got status code 429 with error_type : {result}")
                except Exception as e:
                    print(
                        f"[-] ERROR: WebCreateAjaxAttempt.handle_request() : Got status code 429 with unknown response {self.last_response.text}")
                    print(f"[-] ERROR: WebCreateAjaxAttempt.handle_request() : Got error type {e}")
                finally:
                    time.sleep(15)
                    self.config.proxy_inactive = True
                    return False
            else:
                print(
                    f"[-] ERROR: WebCreateAjaxAttempt.handle_request() : Got unknown status code: {self.last_response.status_code} with unknown response {self.last_response.text}")

                return False
        except Exception as e:
            if "<code>100003</code>" in self.last_response.text:
                print(
                    f"[-] ERROR: WebCreateAjaxAttempt.handle_request(): Unknown Error : status_code : {self.last_response.status_code}\nresponse : {self.last_response.text}")
            print(f"[-] ERROR: WebCreateAjaxAttempt.handle_request() : Got unknown exception {e}")

    def run(self, new):
        if not self.config.info["Cookies"]:
            raise Exception("[-] ERROR: didn\'t get any cookies. WebCreateAjaxAttempt.__init__()")

        if new:
            if self.start_process():
                self.ToString()  # save dict  to file

        else:
            pass
        self.config.info["WebCreateAjaxAttempt"] = {**{"password": self.password}, **self.generate_data(4)}

        print(
            f"Username: {self.config.info['WebCreateAjaxAttempt']['username']}, Password:{self.config.info['WebCreateAjaxAttempt']['password']}, email:{self.config.info['WebCreateAjaxAttempt']['email']}")

    def send_stage(self, stage: int):
        for i in range(2):
            data = self.generate_data(stage)
            self.web_create_ajax_attempt(data)
            if not self.handle_response():
                continue
            else:
                break

    def start_process(self):
        for i in range(1, 5):
            print(f"stage {i} out of 4")
            self.send_stage(i)

    def generate_data(self, times: int) -> dict:
        if times == 1:
            user = {
                'email': self.email,
                'first_name': "",
                'username': "",
                'opt_into_one_tap': self.opt_into_one_tap
            }
        elif times == 2:
            self.update_username()
            user = {
                'email': self.email,
                'first_name': self.first_name,
                'username': "",
                'opt_into_one_tap': self.opt_into_one_tap
            }
        elif times == 3:
            user = {
                'email': self.email,
                'first_name': self.first_name,
                'username': self.username,
                'opt_into_one_tap': self.opt_into_one_tap
            }
        else:
            user = {
                "enc_password": self.enc_password,
                'email': self.email,
                'first_name': self.first_name,
                'username': self.username,
                'opt_into_one_tap': self.opt_into_one_tap
            }

        return user
