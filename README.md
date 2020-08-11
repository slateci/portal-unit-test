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
3. Add the downloaded `chromedriver` executatble to your PATH. For example, if the executatble is located at `/opt/WebDriver/bin`, in `~/.bash_profile` insert the line:
    ```bash
    export PATH=$PATH:/opt/WebDriver/bin
    ```
4. To bypass the notarization requirement on macOS, navigate to the folder of WebDriver. </br>
    *   For `chromedriver` run the following command:
        ```bash
        xattr -r -d com.apple.quarantine chromedriver 
        ```
    *   For `geckodriver` (FireFox) run the following command:
        ```bash
        xattr -r -d com.apple.quarantine geckodriver 
        ```

5. Instantiate a Chrome session in Python using the file path from previous example:
    ```python
    from selenium.webdriver import Chrome

    driver = Chrome('/opt/WebDriver/bin/chromedriver')
    ```


## Run Test
```bash
$ python main.py
```