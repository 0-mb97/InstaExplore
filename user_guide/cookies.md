### Cookies Class Overview:

The `Cookies` class is a fundamental component of the Instagram signup investigation project, responsible for managing cookies essential to maintaining the session state during the account creation process. This class interacts with the Instagram login page to obtain, store, and utilize cookies, ensuring a smooth progression through the various steps of the signup process.

#### Class Initialization:

The `Cookies` class is initialized with parameters such as configuration settings, the username file for which cookies are managed, and optional old values like `csrftoken`, `datr`, and `ig_did`. and new values `mid`, `ig_nrcb`

#### Class Properties:

- **`cookies` Property:**
  - This property serves as both a getter and setter, allowing the management of the `_cookies` attribute.

#### Class Methods:

- **`update_cookie_path(username: str)` Method:**
  - Dynamically updates the path for storing cookies based on the provided username.

- **`get_cookies(username: str = None)` Method:**
  - Retrieves cookies from the specified file based on the provided username.

- **`set_cookies()` Method:**
  - Initiates the process of obtaining and setting cookies by interacting with the Instagram login page.

- **`login_page()` Method:**
  - Sends a request to the Instagram login page and returns the response.

- **`to_string()` Method:**
  - Writes cookies to a JSON file.

- **`run()` Method:**
  - Initiates the cookie handling process.

- **`cookie_handler(load: bool = True)` Method:**
  - Handles cookies, either by loading existing ones or setting new ones.

- **`arrange_cookies_values(mess) -> dict` Method:**
  - Extracts relevant cookie values from the headers and arranges them into a dictionary.

#### Example Usage:

```python
if __name__ == '__main__':
    fake_user_agent = EnhancedFakeUserAgent()
    my_proxy = "some value or none"
    ua = fake_user_agent.get_enhanced_browser("random")
    conf = Config.Config(proxy=my_proxy, user_agent=ua)

    # Initialize PreLogin class with existing configuration
    PreLogin.PreLogin(config=conf, new=False)

    # Initialize Cookies class with a new configuration
    c = Cookies(config=conf, new=True)
    print(c.cookies)

    # Get cookies for a specific username ('first' in this case)
    c.get_cookies(username='first')
    print(c.cookies)

    # Set new cookies
    c.set_cookies()
    print(c.cookies)

