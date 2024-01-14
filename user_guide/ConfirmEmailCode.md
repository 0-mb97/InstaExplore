## Class Overview: ConfirmEmailCode

The `ConfirmEmailCode` class is a pivotal component of the Instagram signup investigation project, meticulously crafted to manage the confirmation of the email code during the account creation process. This class interfaces with the Instagram API to validate the provided confirmation code, facilitating the successful completion of the account creation. It encompasses parameters such as the confirmation code, device ID, and email to verify.

### Class Details

- **Initialization:**
  - Initializes the `ConfirmEmailCode` class with essential parameters, including the confirmation code, device ID, and email to verify.

- **Confirmation Code Verification:**
  - Sends requests to the Instagram API for the verification of the provided confirmation code.
  - Handles various response scenarios, such as rate limiting errors and invalid nonces.

- **Data Generation:**
  - Generates data for the confirmation email request, comprising the confirmation code, device ID, and email to verify.

- **File Handling:**
  - Manages the saving and loading of information to/from a JSON file.
  - Includes the signup code, device ID, and email to verify.

- **Update Configuration:**
  - Updates the configuration information with the latest signup code, confirmation code, device ID, and email to verify.

- **Run Method:**
  - Executes the confirmation code verification process, ensuring multiple attempts and correctness in verification.

### Example Usage

```python
# Basic usage:
def main():
    fake_user_agent = EnhancedFakeUserAgent()
    ua = fake_user_agent.get_enhanced_browser("random")
    my_proxy = "proxy value or none"
    conf = Config(proxy=my_proxy, user_agent=ua)
    PreLogin.PreLogin(conf, new=False)
    Cookies.Cookies(conf, new=False)
    WebCreateAjaxAttempt.WebCreateAjaxAttempt(conf, new=False)
    SendVerifyEmail(config=conf, new=True)
    ConfirmEmailCode(config=conf, new=True)

if __name__ == '__main__':
    main()
```

```python
# manipulate usage: after run basic example
if __name__ == '__main__':
    # Create an instance of the Config class with the specified proxy and user agent
    conf = Config.Config(proxy="your_proxy_value", user_agent="your_user_agent")

    # Initialize the ConfirmEmailCode class with existing configuration
    confirm_email_instance = ConfirmEmailCode(config=conf, new=False)

    # Set custom confirmation code, device ID, and email to verify (optional)
    confirm_email_instance.code = "custom_confirmation_code"
    confirm_email_instance.device_id = "custom_device_id"
    confirm_email_instance.email_to_verify = "custom_email@example.com"

    # Run the ConfirmEmailCode process
    confirm_email_instance.run()

    # Access the result and update the configuration
    result_signup_code = confirm_email_instance.signup_code
    conf.info["ConfirmEmailCode"]["signup_code"] = result_signup_code
    conf.info["ConfirmEmailCode"]["code"] = confirm_email_instance.code
    conf.info["ConfirmEmailCode"]["device_id"] = confirm_email_instance.device_id
    conf.info["ConfirmEmailCode"]["email_to_verify"] = confirm_email_instance.email_to_verify

    # Save the updated configuration to file
    conf.save_config()

