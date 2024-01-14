from fake_useragent import UserAgent


def format_version(version):
    # Convert version to string if it's a float
    version_str = str(version)
    # Ensure the version has 4 digits separated by dots
    version_parts = version_str.split('.')
    while len(version_parts) < 4:
        version_parts.append('0')
    return '.'.join(version_parts[:4])


class EnhancedFakeUserAgent(UserAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enhanced_headers = None

    def get_enhanced_browser(self, request):
        try:
            browser_info = self.getBrowser(request)
            user_agent = browser_info.get("useragent")

            # Extracting version from the user agent
            version = format_version(browser_info.get("version", "0.0.0.0"))
            sec_ch_ua_version = version.split(".")[0]
            self.enhanced_headers = {
                "User-Agent": user_agent,
                "Sec-Ch-Ua": f'"{browser_info["browser"]}";v="{sec_ch_ua_version}", "{browser_info["system"]}";v="{sec_ch_ua_version}"',
                "Sec-Ch-Ua-Platform": browser_info["os"],
                "Sec-Ch-Ua-Full-Version-List": f'"{browser_info["browser"]}";v="{version}", "{browser_info["system"]}";v="{version}"'
            }
            print(self.enhanced_headers)
            return self.enhanced_headers
        except Exception as e:
            print(f"Error occurred during getting browser: {e}")
            raise e


def get_random_useragent():
    fake_user_agent = EnhancedFakeUserAgent()
    return fake_user_agent.get_enhanced_browser("random")
