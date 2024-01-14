import json
from pathlib import Path
import requests
import BuildRequest
from Config import *


class ConfirmEmailCode:
    def __init__(self, config: Config, new: bool = True, filename: str = "last", code=None, device_id=None,
                 email_to_verify=None, data: dict = None):
        self.config = config
        self.data = data
        self.filename = ""
        self.update_filename(filename)
        self.signup_code = None
        self.request = None
        self.last_response = None

        self.code = code if code else self.config.info["SendVerifyEmail"]["code"]
        self.device_id = device_id if device_id else self.config.info["SendVerifyEmail"]["device_id"]
        self.email_to_verify = email_to_verify if email_to_verify else self.config.info["SendVerifyEmail"][
            "email_to_verify"]
        if not new:
            self.read_from_file(filename)

    def generate_confirm_email_request(self):
        data = self.generate_data()
        url = 'https://www.instagram.com/api/v1/accounts/check_confirmation_code/'
        self.request = BuildRequest.BuildRequest(config=self.config, url=url, data=data)

    def send(self):
        try:
            if self.request.send():
                self.last_response = self.request.response
                if isinstance(self.last_response, requests.Response):
                    if self.last_response.text:
                        print(f"[+] INFO: ConfirmEmailCode.send(): server response: {self.last_response.text}")
                    return True
            return False
        except (requests.exceptions.RequestException, TimeoutError) as e:
            print(f"[-] ERROR: ConfirmEmailCode.send() : Got error type {e}")
            return False

    def check_confirmation_code(self):
        self.generate_confirm_email_request()
        for i in range(3):
            if not self.send():
                continue
            result = self.handle_request()
            if result == -1:
                return -1
            elif result:
                return True
        return False

    def handle_request(self):
        try:
            if self.last_response.status_code == 200:
                try:
                    result = json.loads(self.last_response.text)["signup_code"]
                    if result:
                        self.signup_code = result
                        print(f"[+] INFO: ConfirmEmailCode: signup_code is : {self.signup_code}.")
                    else:
                        print(f"[+] INFO: ConfirmEmailCode.handle_request(): signup_code : {result}")
                except Exception as e:
                    print(
                        f"[-] ERROR: ConfirmEmailCode.handle_request() : Got status code 200 with unknown response {self.last_response.text}")
                    print(f"[-] ERROR: ConfirmEmailCode.handle_request() : Got error type {e}")
                finally:
                    return True

            elif self.last_response.status_code == 429 or self.last_response.status_code == 400:
                try:
                    result = json.loads(self.last_response.text)["error_type"]
                    if result == 'rate_limit_error':
                        print(f"[-] ERROR: ConfirmEmailCode.handle_request() : Got status code 429 with error_type : {result}")
                    if result == 'invalid_nonce':
                        print(f"[-] ERROR: ConfirmEmailCode.handle_request() : Got status code 400 with error_type : {result}")
                        return -1
                except Exception as e:
                    print(
                        f"[-] ERROR: ConfirmEmailCode.handle_request() : Got status code 429 with unknown response {self.last_response.text}")
                    print(f"[-] ERROR: ConfirmEmailCode.handle_request() : Got error type {e}")
                finally:
                    time.sleep(15)
                    self.config.proxy_inactive = True
                    return False
            else:
                print(
                    f"[-] ERROR: ConfirmEmailCode.handle_request() : Got unknown status code: {self.last_response.status_code}")
                if self.last_response.text:
                    print(f"with unknown response {self.last_response.text}")
                return False
        except Exception as e:
            print(f"[-] ERROR: ConfirmEmailCode.handle_request() : Got unknown exception {e}")
            return False

    def generate_data(self) -> dict:
        user_info = {
            "code": self.code,
            "device_id": self.device_id,
            "email": self.email_to_verify
        }
        if self.data:
            return {**user_info, **self.data}
        return user_info

    def ToString(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps({"signup_code": self.signup_code, "device_id": self.device_id,
                                "email_to_verify": self.email_to_verify}))
            print("[+] INFO: ConfirmEmailCode.ToString: Done.")
        return True

    def read_from_file(self, file):
        self.update_filename(file)
        if Path.exists(Path(self.filename)):
            with open(self.filename, 'r') as f:
                info = json.load(f)
            self.signup_code = info["signup_code"]
            self.email_to_verify = info["email_to_verify"]
            self.device_id = info["device_id"]
            print("[+] INFO: ConfirmEmailCode.read_from_file(): Done.")
            return True
        else:
            print("[-] Warning: ConfirmEmailCode.read_from_file(): File Name doesnt exist")
            return False

    def update_config(self):
        obj = self.config.info["ConfirmEmailCode"]
        obj["signup_code"] = self.signup_code
        obj["code"] = self.code
        obj["device_id"] = self.device_id
        obj["email_to_verify"] = self.email_to_verify
        print(obj)
        return True

    def run(self):
        if len(self.config.info["SendVerifyEmail"]["code"]) < 4:
            print(f'[-] ERROR: ConfirmEmailCode.run(): code value is : {self.config.info["SendVerifyEmail"]["code"]}')
            return False
        for i in range(2):
            result = self.check_confirmation_code()
            if result == -1:
                return -1
            elif result:
                self.update_config()
                self.ToString()
                return True
        else:
            print("[-] ERROR: ConfirmEmailCode.run(): couldn`t send Confirmation Code correctly")
            return False

    def update_filename(self, filename):
        self.filename = f"create_account/ConfirmEmailCode/{filename}.json"
        print("[+] INFO: ConfirmEmailCode.update_filename(): Done.")
