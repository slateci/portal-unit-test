# Selenium Web App Unit Test on SLATE Portal
[Selenium](https://www.selenium.dev/documentation/en/) is a framework for automating web applications tests. It runs on OS's such as Windows, Mac OS, Linux and Solaris. It's supported browsers include Chrome, FireFox, Edge, Internet Explorer, Safari and Opera. The Selenium client API supports Java, Python, C#, Ruby, JavaScript and Kotlin
## Minimum Requirement
- Operating Systems: Linux or macOS
- Browsers: Chrome or Firefox
- Python 3
- Selenium library for Python
    ```bash
    $ pip install selenium
    ```
- Reference: [Selenium documentation](https://www.selenium.dev/documentation/en/)
## Browser Installation on Linux(CentOS)
- Firefox ([reference](https://tecadmin.net/install-firefox-on-linux/)):
    ```bash
    $ cd /usr/local
    $ sudo wget http://ftp.mozilla.org/pub/firefox/releases/76.0/linux-x86_64/en-US/firefox-76.0.tar.bz2
    $ sudo tar xvjf firefox-76.0.tar.bz2
    $ ln -s /usr/local/firefox/firefox /usr/bin/firefox
    $ rm firefox-76.0.tar.bz2
    ```
    
- Chrome ([reference](https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-centos-7/)):
    ```bash
    $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
    $ sudo yum localinstall google-chrome-stable_current_x86_64.rpm
    $ rm oogle-chrome-stable_current_x86_64.rpm
    ```

## WebDriver Installation
- Referenced [Documentation](https://selenium-python.readthedocs.io/installation.html)
- This instruction assumes the download path is at `/opt/WebDriver/bin`. The users can specify other download path as needed.
### Chrome WebDriver Download
1. Selenium requires a WebDriver of corresponding version to interface with the installed Chrome. Check the installed Chrome version using:
    ```bash
    $ google-chrome --version
    ```
2. For example, if the Chrome version is `84.0.4147.105`, then `ChromeDriver 84.0.4147.30` should be downloaded from [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
    ```bash
    $ cd /opt/WebDriver/bin
    $ sudo wget https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_linux64.zip
    $ sudo unzip chromedriver_linux64.zip
    $ sudo rm chromedriver_linux64.zip
    ```
### Firefox WebDriver Download
* Download the latest [WebDriver for Firefox](https://github.com/mozilla/geckodriver/releases)
    ```bash
    $ cd /opt/WebDriver/bin
    $ sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz
    $ sudo tar xvjf geckodriver-v0.27.0-linux64.tar.gz
    $ sudo rm geckodriver-v0.27.0-linux64.tar.gz
    ```
### Add Download Directory to PATH 
```bash
$ export PATH=$PATH:/opt/WebDriver/bin >> ~/.profile
```
If the above command does not work in macOS, add line `export PATH=$PATH:/opt/WebDriver/bin` to file `~/.bash_profile`

### Check If `PATH` Set Up Correctly
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
### Bypass the notarization requirement on macOS
* macOS notarization requirement can prevent the WebDriver from running
* Navigate to the folder of WebDriver.
* For `chromedriver` run the following command:
    ```bash
    xattr -r -d com.apple.quarantine chromedriver 
    ```
* For `geckodriver` (FireFox) run the following command:
    ```bash
    xattr -r -d com.apple.quarantine geckodriver 
    ```

### Instantiate Chrome and Firefox Sessions In Python 
```python
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

# headless mode set to true to run test in background (VM through ssh)
# headless mode set to false to open a foreground browser session

# test with chrome
ch_options = ChromeOptions()
ch_options.headless = True
ch_driver = Chrome(executable_path='/opt/WebDriver/bin/chromedriver', options=ch_options)

# test with Firefox
ff_options = FirefoxOptions()
ff_options.headless = True 
ff_driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver', options=ff_options)
```

## Test Set Up
This test is set up using the page object pattern detailed in the Selenium-Python documentation. Click this [LINK](https://selenium-python.readthedocs.io/page-objects.html) from reference.

## Tests Structure 
    .
    ├── ...
    ├── main.py                 
    │   ├── PortalBrowsing                          # tests to iterate through web pages
    │   │   ├── test_iterate_clusters_pages
    │   │   ├── test_iterate_apps_pages
    │   │   ├── test_iterate_instances_pages
    │   │   ├── test_iterate_my_groups_pages
    │   │   ├── test_iterate_all_groups_pages
    │   │   └── test_check_cli_access_page
    │   └── FuncTests                               # tests to modify instance/group through the portal
    │       ├── test_add_instance                   # add an Nginx instance
    │       ├── test_instance_delete_accept         # delete the added Nginx instance
    │       ├── test_add_new_group                  # add a "test-group" group
    │       ├── test_edit_group                     # edit "test-group" group
    │       └── test_delete_group                   # delete "test-group" group
    └── ...
## Run Test
To run all tests
```bash
$ python3 main.py
```
To run a type of tests. For example, PortalBrowsing tests
```bash
$ python3 main.py PortalBrowsing
```
To run a specific test. For example, test_instance_delete_accept in FuncTests
```bash
$ python3 main.py FuncTests.test_instance_delete_accept
```