from EnhancedFakeUserAgent import EnhancedFakeUserAgent


class Config:

    def __init__(self, user_agent: dict = None, proxy: dict = None, cookies: dict = None, method=None,
                 x_instagram_ajax=None, fake_cookies=None):
        self.info = {
            "PreLogin": {

            },
            "Cookies": {

            },
            "WebCreateAjaxAttempt": {

            },
            "SendVerifyEmail": {

            },
            "ConfirmEmailCode": {

            },
            "CreateAccountAjax": {

            }

        }
        self.user_agent = user_agent
        self.proxy = proxy
        self.method = method
        self.cookies = cookies
        self.fake_cookies = fake_cookies
        self.x_instagram_ajax = x_instagram_ajax
        self.proxy_inactive = False

    def set_useragent(self):
        self.user_agent = EnhancedFakeUserAgent().get_enhanced_browser("random")

    def set_proxy(self,value:dict):
        self.proxy = value
