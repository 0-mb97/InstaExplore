import time
import requests
from BuildRequest import BuildRequest
from Config import Config
from CreateAccountFunctions import extract_code_from_html


class FakeMail:
    MAX_RETRIES = 6

    def __init__(self, conf: Config, mail):
        self.conf = conf
        self.mail = mail
        self.last_response = None
        self.request = None
        self.code = None

    def generate_request(self):
        url = 'https://email-fake.com/'
        mail, domain = self.mail.split("@")
        self.conf.fake_cookies = f'{domain}%2F{mail}'
        self.request = BuildRequest(config=self.conf, url=url)

    def send(self):
        try:
            if self.request.send():
                self.last_response = self.request.response
                if isinstance(self.last_response, requests.Response):
                    print(f"[+] INFO: FakeMail.send() : In Process")
                    return True
            return False
        except (requests.exceptions.RequestException, TimeoutError) as e:
            print(f"[-] ERROR: FakeMail.send() : Got error type {e}")
            return False

    def handle_response(self):
        try:
            status_code = self.last_response.status_code

            if status_code == 200:
                # return value is tuple[code][date]
                code_test = extract_code_from_html(self.last_response.text)
                if code_test:
                    print(f"[+] INFO: FakeMail.handle_response(): Got status code with code value is {code_test}")
                    self.code = code_test
                    return True
                else:
                    print(f"[-] ERROR: FakeMail.handle_response(): Got status code but code value is {code_test}")
                    time.sleep(8)
                    return False
            else:
                print(
                    f"[-] ERROR: FakeMail.handle_response(): Request failed unknown with status code: {status_code}. retrying "
                    f"without proxy")
                self.conf.proxy_inactive = True
                return False
        except Exception as e:
            print(f"[-] ERROR: FakeMail.handle_response(): {e}")
            # print(f"[-] ERROR: FakeMail.handle_response(): request end up without response : {self.last_response}. Retrying...")
            return False

    def retrieve_fakemail_code(self):

        for i in range(self.MAX_RETRIES):
            if self.send():
                if self.handle_response():
                    return True
                else:
                    continue
            else:
                time.sleep(8)
                continue
        return False

    def get_code_from_mail(self):
        self.generate_request()

        for i in range(2):
            if self.retrieve_fakemail_code():
                return self.code
        return False
