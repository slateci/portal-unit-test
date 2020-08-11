## SLATE Portal Web Application Unit Test Using Selenium
[Selenium](https://www.selenium.dev/documentation/en/) is a framework for automating web applications tests. It runs on OS's such as Windows, Mac OS, Linux and Solaris. It's supported browsers include Chrome, FireFox, Edge, Internet Explorer, Safari and Opera. The Selenium client API supports Java, Python, C#, Ruby, JavaScript and Kotlin
## Test Environment Set Up
The test was developed on Mac OS, using Chrome web browser and Python. For test set up using other OS and/or browsers, please refer to the [Selenium documentation](https://www.selenium.dev/documentation/en/)
### Install Selenium library for Python
```bash
$ pip install selenium
```
### Install WebDriver binary
1. Selenium requires a corresponding driver to interface with the choosen drive. To download the correct driver, click this [Selenium-Python documentation](https://selenium-python.readthedocs.io/installation.html)
2. For example, if the Chrome used for testing is at version `84.0.4147.105`, then download the `ChromeDriver 84.0.4147.30` from [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
3. Add the downloaded WebDriver to your `PATH`. For example, if the executatble is at `/opt/WebDriver/bin`, 
    * for macOS and linux enter the following command:
        ```bash
        $ export PATH=$PATH:/opt/WebDriver/bin >> ~/.profile
        ```
    * if the above command does not work in macOS, add the line below in `~/.bash_profile`
        ```bash
        export PATH=$PATH:/opt/WebDriver/bin
        ```
    * check if the `PATH` is set up correctly:
        * for `chromedriver`, enter `chromedriver` in terminal. The terminal should output:
            ```bash
            Starting ChromeDriver 84.0.4147.30 (48b3e868b4cc0aa7e8149519690b6f6949e110a8-refs/branch-heads/4147@{#310}) on port 9515
            Only local connections are allowed.
            Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
            ChromeDriver was started successfully.      
            ```
        * for `geckodriver`, enter `geckodriver` in terminal. The terminal should output:
            ```bash
            1597169870563	geckodriver	INFO	Listening on 127.0.0.1:4444
            ```

4. To bypass the notarization requirement on macOS, navigate to the folder of WebDriver. </br>
    * For `chromedriver` run the following command:
        ```bash
        xattr -r -d com.apple.quarantine chromedriver 
        ```
    * For `geckodriver` (FireFox) run the following command:
        ```bash
        xattr -r -d com.apple.quarantine geckodriver 
        ```

5. Instantiate a Chrome session in Python using the file path from previous example:
    ```python
    from selenium.webdriver import Chrome

    driver = Chrome('/opt/WebDriver/bin/chromedriver')
    ```

## Test Set Up
This test is set up using the page object pattern detailed in the Selenium-Python documentation. Click this [LINK](https://selenium-python.readthedocs.io/page-objects.html) from reference.

## Run Test
```bash
$ python main.py
```