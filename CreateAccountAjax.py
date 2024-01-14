from datetime import datetime

import requests

from WebCreateAjaxAttempt import *
from CreateAccountFunctions import check_username_in_title, generate_new_fake_mail


class CreateAccountAjax:
    def __init__(self, config: Config, filename: str = "ig_account", enc_password=None, day=None, email=None,
                 first_name=None, month=None,
                 client_id=None, seamless_login_enabled=1, tos_version="row", signup_code=None, username=None,
                 year=None, password=None, data: dict = None):
        self.config = config
        self.request = None
        self.last_response = None
        self.data = data
        self.filename = f"{filename}.txt"

        self.password = password if password else config.info["WebCreateAjaxAttempt"]["password"]
        self.enc_password = enc_password if enc_password else config.info["WebCreateAjaxAttempt"]["enc_password"]
        self.email = email if email else config.info["ConfirmEmailCode"]["email_to_verify"]
        self.first_name = first_name if first_name else config.info["WebCreateAjaxAttempt"]["first_name"]
        self.username = username if username else config.info["WebCreateAjaxAttempt"]["username"]
        self.day = day if day else random.randint(1, 27)
        self.month = month if month else random.randint(1, 12)
        self.year = year if year else random.randint(1960, 1999)
        self.client_id = client_id if client_id else config.info["ConfirmEmailCode"]["device_id"]
        self.seamless_login_enabled = seamless_login_enabled
        self.tos_version = tos_version
        self.signup_code = signup_code if signup_code else config.info["ConfirmEmailCode"]["signup_code"]

    def save_credential(self, filename=None):
        if not filename:
            filename = f"{self.filename}.txt"
        with open(filename, "a") as f:
            acc = f"{self.username}:{self.password}:{self.first_name}:{self.email} >> {self.last_response.status_code} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f.write(acc)
            print(acc)

    def check_username(self):
        try:
            account_user = check_username_in_title(self.username, self.config)
            if account_user:
                self.save_credential()
                print(f"[+] INFO: CreateAccountAjax: account_created : True .")
            elif account_user is None:
                self.save_credential(filename="ig_error.txt")
                print(
                    f"[+] INFO: CreateAccountAjax: account_created : Check it later, Credential saved into ig_error.txt")
            else:
                print(
                    f"[+] INFO: CreateAccountAjax: account_created : False, Credential saved into ig_no_login.txt")
                self.save_credential(filename="ig_no_login.txt")
        except Exception as e:
            self.save_credential(filename="ig_error.txt")
            print(f"[-] ERROR: CreateAccountAjax.check_username(): Exception info {e}")

    def generate_request(self):
        data = self.generate_data()
        url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/"
        self.request = BuildRequest.BuildRequest(config=self.config, url=url, data=data)

    def send(self):
        try:
            if self.request.send():
                self.last_response = self.request.response
                if isinstance(self.last_response, requests.Response):
                    return True
            return False
        except (requests.exceptions.RequestException, TimeoutError) as e:
            print(f"[-] ERROR: CreateAccountAjax.send() : Got error type {e}")
            return False

    def handle_request(self):
        try:
            if self.last_response.status_code == 200:
                try:
                    print(self.last_response.text)
                    result = json.loads(self.last_response.text)
                    if result["account_created"] is True:
                        self.check_username()
                        return True
                    elif result["account_created"] is False:
                        if result["error_type"] == "signup_block":
                            print(f"[-] ERROR: CreateAccountAjax.handle_request(): IP is blocked")
                            # perform rotate ip instead of raise exception
                            raise Exception("IP is blocked")
                        elif result["error_type"] == "form_validation_error":
                            # Changing username:
                            wc = WebCreateAjaxAttempt(config=self.config, new=False)
                            self.username = wc.get_username_from_list()
                            print(f"[+] INFO: CreateAccountAjax.handle_request(): changed_username : {self.username}")
                            # Changing email:
                            self.email = generate_new_fake_mail(self.config.proxy)
                            print(f"[+] INFO: CreateAccountAjax.handle_request(): changed_mail : {self.email}")
                            return False
                        else:
                            print(f"[-] ERROR: CreateAccountAjax.handle_request() : Got status code 200 with unknown "
                                  f"response {self.last_response.text}")
                except Exception as e:
                    print(
                        f"[-] ERROR: CreateAccountAjax.handle_request() : Got status code 200 with error type {e}\n{self.last_response.text if self.last_response.text else 'no payload'}")

            elif self.last_response.status_code == 429:
                try:
                    result = json.loads(self.last_response.text)["error_type"]
                    if result == 'rate_limit_error':
                        print(
                            f"[-] ERROR: CreateAccountAjax.handle_request() : Got status code 429 with error_type : {result}")
                except Exception as e:
                    print(
                        f"[-] ERROR: CreateAccountAjax.handle_request() : Got status code 429 with unknown response {self.last_response.text}")
                    print(f"[-] ERROR: CreateAccountAjax.handle_request() : Got error type {e}")
                finally:
                    time.sleep(15)
                    self.config.proxy_inactive = True
                    return False
            else:
                print(
                    f"[-] ERROR: CreateAccountAjax.handle_request() : Got unknown status code: {self.last_response.status_code}")
                if self.last_response.text:
                    print(f"with unknown response {self.last_response.text}")
                self.check_username()
                return True
        except Exception as e:
            print(f"[-] ERROR: CreateAccountAjax.handle_request() : Got unknown exception {e}")
            self.check_username()
            return False

    def create_account_ajax(self):
        self.generate_request()
        for i in range(3):
            if not self.send():
                continue
            print("[+] INFO: CreateAccountAjax.send() : Done.")

            if self.handle_request():
                print("[+] INFO: CreateAccountAjax.handle_request() : Done.")
                return True
            else:
                continue
        return False

    def run(self):
        try:
            if self.create_account_ajax():
                self.update_config()
                return True
            return False
        except Exception as e:
            print(f"[-] ERROR: CreateAccountAjax.run() : Got unknown exception {e}")

    def update_config(self):
        self.config.info["CreateAccountAjax"] = self.generate_data()

    def generate_data(self) -> dict:
        user_info = {
            "enc_password": self.enc_password,
            "day": self.day,
            "email": self.email,
            "first_name": self.first_name,
            "month": self.month,
            "username": self.username,
            "year": self.year,
            "client_id": self.client_id,
            "seamless_login_enabled": self.seamless_login_enabled,
            "tos_version": self.tos_version,
            "force_sign_up_code": self.signup_code,
        }
        if self.data:
            return {**user_info, **self.data}
        return user_info
