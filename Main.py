from requests.exceptions import InvalidProxyURL
from ConfirmEmailCode import ConfirmEmailCode
from CreateAccountAjax import CreateAccountAjax
from SendVerifyEmail import SendVerifyEmail
from Cookies import Cookies
from PreLogin import PreLogin
from CreateAccountManager import CreateAccountManager, handle_exception
from pathlib import Path
import logging
import requests

from WebCreateAjaxAttempt import WebCreateAjaxAttempt


def dir_path_verify():
    """
    Function to create necessary directories and files
    """
    # Directories to be created
    create_dir = ["cookies", "pre_login", "ConfirmEmailCode", "SendVerifyEmail", "WebCreateAjaxAttempt",
                  "logs/main.log"]
    # Files to be created
    create_file = ["proxies.txt", "ig_account.txt", "ig_errors.txt", "ig_no_login.txt", "used_proxies"]

    # Create directories
    for f in create_dir:
        try:
            directory_path = Path(f"create_account/{f}")
            directory_path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            pass

    # Create files
    for j in create_file:
        file_path = Path(j)
        if not file_path.exists():
            # Create the file if it doesn't exist
            file_path.touch()


class run(CreateAccountManager):
    def __init__(self, name, proxy_amount: int):
        """
        Main class to run the account creation process
        """
        super().__init__(name, proxy_amount)

    def start(self):
        """
        Set user-agent for the requests
        """
        try:
            self.set_useragent()
        except (requests.exceptions.RequestException, TimeoutError):
            pass
        return True

    def run(self):
        """
        Execute the main account creation process
        Here you can modify the value of parameters of each request
        by initial the object with your own process, or choose file=your_file to read values from file,
        or choose new=False  to use the last saved details.
        """
        try:
            # Execute the pre-login steps
            PreLogin(config=self.config, new=True)
            Cookies(config=self.config, new=True)
            WebCreateAjaxAttempt(config=self.config, new=True)
            SendVerifyEmail(config=self.config).run()
            try:
                # Handle email confirmation codes
                # Retry up to 3 times if no message found in mail
                for j in range(3):
                    if ConfirmEmailCode(config=self.config).run() == -1:
                        SendVerifyEmail(config=self.config).run()
                    else:
                        break
                # Create an Instagram account
                CA = CreateAccountAjax(config=self.config).run()
                return CA
            except Exception:
                return False
        except Exception as e:
            print(e)
            handle_exception(e)
            return False

    def final(self):
        """
        Placeholder for any finalization steps
        """
        pass

    def run_Handler(self):
        """
        Main handler to start the account creation process
        """
        try:
            # Log information, start the process, and handle exceptions
            self.ToString()
            if not self.start():
                logging.warning("User-Agent not set.")
            self.last_result = self.run()
            self.final()
            return True

        except (OSError, requests.RequestException, InvalidProxyURL) as e:
            logging.error("Error: %s", e)
            handle_exception(e)
            return False
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)
            handle_exception(e)
            return False


if __name__ == '__main__':
    # Verify and create necessary directories and files
    dir_path_verify()
    # Change proxy_path to define which file the program will read the proxies.
    proxy_path = "proxies"
    # Instantiate and run the main process
    ca = run(name="client_0", proxy_amount=0)
    ca.run_Handler()
