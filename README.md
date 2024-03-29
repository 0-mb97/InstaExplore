## README.md

# InstaExplore: Instagram Signup Research Tool

Welcome to InstaExplore, a Python project conceived during SwordsWar! This dedicated tool aims to contribute to ongoing challenges in social networks by focusing on the intricate process of Instagram signup. Through meticulous simulation of various steps, InstaExplore provides users with the means to explore and comprehend the complexities of the signup flow.

## Key Features:

1. **In-depth Investigation:**
   - Explore the intricacies of the Instagram signup process through meticulous simulations of various steps.

2. **Meticulous Simulation:**
   - Simulate various signup steps with precision, providing a detailed understanding of the process.

3. **Comprehend Signup Flow Complexities:**
   - Gain insights into the complexities of the Instagram signup flow, allowing for a comprehensive understanding.

Discover and analyze the Instagram signup process like never before with InstaExplore!


## Overview:

1. **Configurable Settings:**
   - Tailor user agents, proxies, cookies, and other parameters in each step of the process. Manipulate the data from a configuration file (`main.py`).
   - Upon the first run, the payload request is saved to a customization file.
   - In subsequent runs, choose whether to read data from the file or server, offering flexibility in the investigation process. Each class request contains several parameters that can be modified in `main.py`, and additional data can be seamlessly added to requests.

2. **Class Overview:**

   - **CreateAccountManager:**
Responsible for managing client-side configuration.
     - Control proxies, user-agents, and IP tracking during the Instagram account creation process. Integrates OpenVPN configurations, handles user-agents, and ensures dynamic proxy switching for a realistic signup simulation.

   - **[PreLogin](./user_guide/pre_login.md):** Handles pre-login actions.
      - Manages actions required before the actual login process, including obtaining initial session information such as js_ig_did, js_datr, csrftoken, and x_instagram_ajax.

   - **[Cookies](./user_guide/cookies.md):** Manages cookies for the Instagram session.
      - Crucial for maintaining session state, this class handles the management of cookies, ensuring necessary session data is retained throughout the signup process, including initial session information such as mid and ig_nrcb.

   - **[WebCreateAjaxAttempt](./user_guide/WebCreateAjaxAttempt.md):** Manages attempts to create a new Instagram account via web AJAX.
      - Handles the creation of an Instagram account through asynchronous requests, managing data such as the username, first_name, password, enc_password, email, opt_into_one_tap, automatically set by the program.

   - **[SendVerifyEmail](./user_guide/SendVerifyEmail.md):** Sends verification emails.
      - Manages the step of sending verification emails, handling data such as email_to_verify, device_id, and retrieving the code from fake-mail.com automatically.

   - **[ConfirmEmailCode](./user_guide/ConfirmEmailCode.md):** Handles confirmation of the verification code.
      - Manages the process of confirming the verification code received via email. Handles user input, validation, and interaction with the verification code, sending the code along with previous parameters.

   - **[CreateAccountAjax](./user_guide/CreateAccountAjax.md):** Creates a new Instagram account through the web AJAX process.
      - Contains parameters from previous steps and adds the signup_code. It manages data such as username, password, email, and other parameters.

3. **Logging and Output:**
   - The project generates detailed logs (`logs/main.log`) for each step.
   - Output files, such as account information and errors, are saved for analysis.
## Usage

   - Install required dependencies using `pip install -r requirements.txt`.
   - create `./create_account/logs` folder to avoid errors
   - Use `main.py` to run specific classes corresponding to desired signup process steps.
   - Detailed instructions for each step are provided within the source code comments.


## Examples
check the file [Main.py](Main.py)

## Disclaimer
   - This tool is for research purposes only.
   - Unauthorized or illegal use is strictly prohibited.
   - Contributors and maintainers are not responsible for misuse or consequences.

## License
   - Licensed under the MIT License.

## How to Contribute

Excited to contribute? We'd love to have you on board! Follow these steps:


1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.

Feel free to reach out if you have any questions or suggestions. Happy coding!


