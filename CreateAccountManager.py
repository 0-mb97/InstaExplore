import OpenVPNManager
from SendVerifyEmail import *



def get_proxy_from_file(proxy_source="proxies"):
    """

    :param proxy_source: proxy_file_source
    :return: first line of file. delete proxy_path value, and write it to used_proxies.txt
    """
    with open(proxy_source, 'r') as f:
        first_proxy = f.readline().strip()
    # Write the first proxy to used_proxies_file
    with open("used_proxies", 'a') as f:
        f.write(f"{first_proxy}\n")
    # Remove the first line from proxies_file
    with open(proxy_source, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(proxy_source, 'w') as fout:
        fout.writelines(data[1:])
    return first_proxy


def set_proxy(value):
    if value:
        return {'http': f'http://{value}', 'https': f'http://{value}'}
    print("[-] ERROR: CreateAccountManager.set_proxy(): Got None as value")
    return None


def handle_exception(e):
    with open("exception", "a") as f:
        f.write(f"{e}\n")


class CreateAccountManager:

    def __init__(self, name, proxy_amount: int):
        self.proxy_pointer = 0
        self.config = Config.Config()
        self.proxy_list = [set_proxy(get_proxy_from_file()) for _ in range(proxy_amount)]
        self.old_ip = ""
        self.last_result = None
        self.name = name
        self.old_useragent = []

    def set_ovpn(self, path: str, root: str):
        self.config.ovpn = OpenVPNManager.OpenVPNManager(config_path=path, password=root)

    @timeout(20)
    def set_useragent(self):
        attempts = -1
        try:
            print("[+] searching for useragent...")
            self.config.set_useragent()
            while self.config.user_agent in self.old_useragent:
                attempts += 1
                if attempts > 20:
                    self.old_useragent = []
                self.config.set_useragent()
            self.old_useragent.append(self.config.user_agent)
        except TimeoutError:
            print("couldnt find different useragent")

    def update_proxy_pointer(self):
        value = self.proxy_pointer + 1
        if value >= len(self.proxy_list):
            value = 0
        self.proxy_pointer = value

    def change_proxy(self, location: int = None):
        """
        when the amount of proxy_list is bigger than 1, you can switch between proxies.
        :param location: the location of chosen proxy in self.proxy_list.
        :return: set the proxy value in self.proxy_list
        """
        submit = None
        for j in range(2):
            try:
                if location and 0 <= location < len(self.proxy_list):
                    new_proxy = self.proxy_list[location]
                else:
                    new_proxy = self.proxy_list[self.proxy_pointer]
                    self.update_proxy_pointer()

                self.config.set_proxy(new_proxy)
                print('New proxy set:', new_proxy)
                submit = True
            except IndexError:
                print("[-] Error: CreateAccountManager.change_proxy(): Invalid location provided.")
                continue
            except Exception as e:
                print(f"[-] Error: CreateAccountManager.change_proxy(): {e}")
                continue
            finally:
                if submit:
                    return True
                else:
                    location = None
                    continue

    def ToString(self):
        print(f"name: {self.name}, last_ip: {self.old_ip}, proxy: {self.config.proxy}")

    def get_external_ip(self):
        ip_services = [
            'https://ifconfig.me/ip',
            'https://ipinfo.io/ip',
            'https://api64.ipify.org'
        ]

        for service in ip_services:
            logging.debug("Fetching IP from %s", service)
            try:
                response = requests.get(service, proxies=self.config.proxy, timeout=30, verify=False)
                if response.status_code == 200:
                    return response.text.strip()

                else:
                    raise requests.RequestException
            except (requests.RequestException, TimeoutError) as e:
                logging.error("Error fetching IP from %s: %s", service, str(e))
                continue
        logging.error("Failed to retrieve external IP from all services.")
        return None

    @timeout(60)
    def wait_until_switch_ip(self):
        """
        in case your proxy server support ip rotate, you can verify the ip changed before you start to run.
        :return: True. when new ip discovered.
        """
        try:
            # logging.info("wait_until_switch_ip()")
            logging.info("Old IP: %s", self.old_ip)
            logging.info("Waiting for a new IP...")
            new_ip = self.get_external_ip()
            while self.old_ip == new_ip or new_ip is None:
                time.sleep(10)
                try:
                    new_ip = self.get_external_ip()
                except Exception as e:
                    logging.warning("Error getting new IP: %s", str(e))

            self.old_ip = new_ip
            logging.info("New IP: %s", new_ip)
            return True
        except TimeoutError:
            logging.error("Timeout error occurred.")
            return True
        except Exception as e:
            logging.error("An unexpected error occurred: %s", str(e))
            handle_exception(f"wait_until_switch_ip() : {e}")
            return True
