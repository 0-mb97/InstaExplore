import logging
from typing import Dict, Optional
from FakeMail import FakeMail
from CreateAccountFunctions import *
from WebCreateAjaxAttempt import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("create_account/logs/main.log"),
        logging.StreamHandler()
    ]
)


class SendVerifyEmail:
    MAX_RETRIES = 6

    def __init__(self, config: Config, new: bool = True, filename="last.json", email_to_verify=None, device_id=None):
        self.config = config
        self.filename = filename
        self.update_filename(filename)

        self.result = None
        self.last_response = None
        self.request = None

        self.last_code = ["", ""]
        self.device_id = device_id if device_id else self.config.info["Cookies"]["mid"]
        self.email_to_verify = email_to_verify if email_to_verify else self.config.info["WebCreateAjaxAttempt"]["email"]
        if not new:
            self.read_from_file(filename)

    def set_device_id(self, value):
        self.device_id = value
        self.ToString()

    def get_device_id(self):
        return self.device_id

    def set_email_to_verify(self, value):
        self.email_to_verify = value
        print()
        self.ToString()

    def get_email_to_verify(self):
        return self.email_to_verify

    def generate_data(self, data: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        user_info = {
            "device_id": self.device_id,
            "email": self.email_to_verify
        }
        if data:
            return {**user_info, **data}
        return user_info

    def generate_verify_email_request(self, add_my_data=None):
        data = self.generate_data(add_my_data)
        url = "https://www.instagram.com/api/v1/accounts/send_verify_email/"
        self.request = BuildRequest.BuildRequest(config=self.config, url=url, data=data)

    def send(self):
        try:
            if self.request.send():
                self.last_response = self.request.response
                if isinstance(self.last_response, requests.Response):
                    return True
            return False
        except (requests.exceptions.RequestException, TimeoutError) as e:
            print(f"[-] ERROR: SendVerifyEmail.send() : Got error type {e}")
            return False

    def send_verify_email(self, data=None):
        self.generate_verify_email_request(add_my_data=data)
        for i in range(3):
            if not self.send():
                continue
            if self.handle_request():
                return True
        return False

    def is_code_new(self, code_test):
        if self.last_code[1] != code_test[1]:
            self.last_code = code_test
            self.result = self.last_code[0]
            print(f"[+] INFO: SendVerifyEmail.is_code_new(): Done.\nThe new code is {self.result}")
            return True
        else:
            print(f"[+] INFO: SendVerifyEmail.is_code_new(): Still In Process. Retrying..")
            return False

    def handle_request(self):
        try:
            if self.last_response.status_code == 200:
                try:
                    result = json.loads(self.last_response.text)["email_sent"]
                    if result is True:
                        print(f"[+] INFO: SendVerifyEmail: email_sent : Done.")
                    else:
                        print(f"[+] INFO: SendVerifyEmail: email_sent : {result}")

                except Exception as e:
                    print(
                        f"[-] ERROR: SendVerifyEmail.handle_request() : Got status code 200 with unknown response {self.last_response.text}")
                    print(f"[-] ERROR: SendVerifyEmail.handle_request() : Got error type {e}")
                finally:
                    return True

            elif self.last_response.status_code == 429:
                try:
                    result = json.loads(self.last_response.text)["error_type"]
                    if result == 'rate_limit_error':
                        print(
                            f"[-] ERROR: SendVerifyEmail.handle_request() : Got status code 429 with error_type : {result}")
                except Exception as e:
                    print(
                        f"[-] ERROR: SendVerifyEmail.handle_request() : Got status code 429 with unknown response {self.last_response.text}")
                    print(f"[-] ERROR: SendVerifyEmail.handle_request() : Got error type {e}")
                finally:
                    time.sleep(15)
                    self.config.proxy_inactive = True
                    return False
            else:
                print(
                    f"[-] ERROR: SendVerifyEmail.handle_request() : Got unknown status code: {self.last_response.status_code} with unknown response {self.last_response.text}")
                return False
        except Exception as e:
            print(f"[-] ERROR: SendVerifyEmail.handle_request() : Got unknown exception {e}")

    def get_code_from_mail(self, fakemail: FakeMail):
        for i in range(2):
            code = fakemail.get_code_from_mail()
            if not code:
                time.sleep(40)
                self.send_verify_email()
                continue
            elif len(code[0]) == 6:
                return code
        return False

    def ToString(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps(
                {"email_to_verify": self.email_to_verify, "device_id": self.device_id, "code": self.last_code}))
            print(f"[+] INFO: SendVerifyEmail.ToString(): Done.")
        return True

    def read_from_file(self, filename):
        self.update_filename(filename)
        if Path(self.filename).exists():
            try:
                with open(self.filename, 'r') as f:
                    info = json.load(f)
                self.email_to_verify = info["email_to_verify"]
                self.device_id = info["device_id"]
                self.last_code = info["code"]
                print(f"[+] INFO: SendVerifyEmail.read_from_file(): Done.")
                return True
            except json.JSONDecodeError as e:
                logging.error(f"[-] ERROR: SendVerifyEmail.read_from_file(): Error decoding JSON: {e}")
                return False
            except Exception as e:
                print(f"[-] ERROR: SendVerifyEmail.read_from_file(): An unexpected error occurred: {e}")
                return False
        else:
            print("[!] Warning: SendVerifyEmail.read_from_file(): File does not exist. continue with default values")
            return True

    def run(self):

        if self.send_verify_email():
            fakemail = FakeMail(conf=self.config, mail=self.email_to_verify)
            for i in range(5):
                value = self.get_code_from_mail(fakemail)
                if value is False:
                    return False
                else:
                    if self.is_code_new(value):
                        self.update_config()
                        self.ToString()
                        return True
                    else:
                        time.sleep(8)
                        continue
            return False
        else:
            return None

    def update_config(self):
        obj = self.config.info["SendVerifyEmail"]
        obj["code"] = self.result
        obj["device_id"] = self.device_id
        obj["email_to_verify"] = self.email_to_verify
        print(obj)
        return True

    def update_filename(self, file):
        self.filename = f"create_account/SendVerifyEmail/{file}"
