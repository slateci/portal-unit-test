# Selenium Web App Unit Test on SLATE Portal

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

> **_IMPORTANT:_** This test suite adds and removes test data. Do not run on against a production Portal instance.

[Selenium](https://www.selenium.dev/documentation/en/) is a framework for automating web applications tests. It runs on OS's such as Windows, Mac OS, Linux and Solaris. It's supported browsers include Chrome, FireFox, Edge, Internet Explorer, Safari and Opera. The Selenium client API supports Java, Python, C#, Ruby, JavaScript and Kotlin.

This test is set up using the [page object pattern](https://selenium-python.readthedocs.io/page-objects.html) detailed in the Selenium-Python documentation.

## Test Suite Structure
    .
    ├── ...
    ├── main.py                 
    │   ├── PortalBrowsing                          # tests to iterate through web pages
    │   │   ├── test_iterate_clusters_pages
    │   │   ├── test_iterate_apps_pages
    │   │   ├── test_iterate_instances_pages
    │   │   ├── test_iterate_secrets_pages
    │   │   ├── test_iterate_my_groups_pages
    │   │   ├── test_iterate_all_groups_pages
    │   │   └── test_check_cli_access_page
    │   └── FuncTests                               # tests to modify instance/group through the portal
    │       ├── test_add_and_delete_instance        # add and delete an Nginx instance
    │       ├── test_add_instance_wrong_input       # try adding an Nginx instance with wrong input
    │       ├── test_add_and_delete_group           # add and delete a new group
    │       ├── test_add_group_wrong_input          # try adding a group with wrong input
    │       ├── test_edit_group                     # edit "test-group" group
    │       ├── test_edit_group_wrong_input         # try editing a group with wrong input
    │       ├── test_edit_cluster_in_group (in progress)
    │       ├── test_add_group_to_cluster           # allow a group to access the cluster
    │       ├── test_revoke_group_from_cluster      # revoke a group's access to the cluster
    │       ├── test_add_and_delete_secret          # add and delete a secret
    │       └── test_add_secret_wrong_input         # trying adding a secret with wrong input
    └── ...

## Running the Test Suite

### GitHub Actions

In the [slateci-portal repo](https://github.com/slateci/slate-portal), the GitHub Actions testing procedure is set up in [selenium-tests.yml](https://github.com/slateci/slate-portal/blob/master/.github/workflows/selenium-tests.yml). The test is set up tp run on `push` or `pull request` to the `master` branch of the [slateci.io repository](https://github.com/slateci/slateci.github.io). Below is the list of the test setup and running procedure:
1. Setup Python 3.8
2. Install Selenium Python bindings
3. Install Chrome web driver. After installation, the path to the web driver will be at `/home/runner/work/slateci.github.io/slateci.github.io/chromedriver`
4. Download Selenium test. The test program in this repository will be downloaded to the GitHub Actions VM in the [slateci-portal repo](https://github.com/slateci/slate-portal)
5. Run Selenium Tests
6. Post Slack to `#website` if the test failed.

### Docker

Run the test suite against a clean local Portal instance (default: `http://localhost:5050/slate_portal`):

```shell
[your@localmachine ~]$ docker run -it -v $PWD:/opt/project --network="host" hub.opensciencegrid.org/slate/python-chromedriver-selenium:3.9-debian python main.py
INFO     3) test_add_and_delete_group
INFO     3) test_add_and_delete_group
INFO     3) test_add_and_delete_group
INFO     adding group test-add-and-delete-group for delete group test
INFO     adding group test-add-and-delete-group for delete group test
INFO     adding group test-add-and-delete-group for delete group test
...
...
```

or specify a different Portal instance URL via `python main.py <url>`.

* Use the `$PWD:/opt/project` volume to mount files from the host to the container.
* The Python installation in the image may be used as a remote interpreter in IDEs such as [VSCode](https://devblogs.microsoft.com/python/remote-python-development-in-visual-studio-code/) and [IntelliJ](https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html).
* Refer to [slateci/slate-portal](https://github.com/slateci/slate-portal) and [minislate](https://github.com/slateci/minislate) for additional information on running the Portal locally.

#### Troubleshooting

The webdriver is containerized and that unfortunately means running it without `options.add_argument('--headless')` will not work without a lot of extra steps. However, using screenshots can sometimes help isolate an issue. Drop code like the following into a desired location in the test suite.

```python
###########################################
import time
now = int(time.time())
self.driver.save_screenshot('/opt/project/screenshots/{}.png'.format(now))
###########################################
```

* Access the images in `$PWD/screenshots` (ignored by Git).
* **Note:** Since the container is running as `root` Linux hosts will need to use `sudo` to remove the files or run `rm screenshots/*` from within the container itself.

### Local Machine

#### Minimum Requirements

* Operating Systems: Linux or macOS
* Browsers: Chrome or Firefox
* Python 3
* Selenium library for Python
  ```bash
  $ pip install selenium
  ```
* Reference: [Selenium documentation](https://www.selenium.dev/documentation/en/)

#### Browser Installation on Linux(CentOS)

* Firefox ([reference](https://tecadmin.net/install-firefox-on-linux/)):
  ```bash
  $ cd /usr/local
  $ sudo wget http://ftp.mozilla.org/pub/firefox/releases/76.0/linux-x86_64/en-US/firefox-76.0.tar.bz2
  $ sudo tar xvjf firefox-76.0.tar.bz2
  $ ln -s /usr/local/firefox/firefox /usr/bin/firefox
  $ rm firefox-76.0.tar.bz2
  ```

* Chrome ([reference](https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-centos-7/)):
  ```bash
  $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
  $ sudo yum localinstall google-chrome-stable_current_x86_64.rpm
  $ rm oogle-chrome-stable_current_x86_64.rpm
  ```

#### WebDriver Installation

* Referenced [Documentation](https://selenium-python.readthedocs.io/installation.html)
* This instruction assumes the download path is at `/opt/WebDriver/bin`. The users can specify other download path as needed.

##### Chrome WebDriver Download

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

#### Firefox WebDriver Download

Download the latest [WebDriver for Firefox](https://github.com/mozilla/geckodriver/releases):

```bash
$ cd /opt/WebDriver/bin
$ sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz
$ sudo tar xvjf geckodriver-v0.27.0-linux64.tar.gz
$ sudo rm geckodriver-v0.27.0-linux64.tar.gz
```

#### Add Download Directory to PATH

```bash
$ export PATH=$PATH:/opt/WebDriver/bin >> ~/.profile
```

If the above command does not work in macOS, add line `export PATH=$PATH:/opt/WebDriver/bin` to file `~/.bash_profile`.

#### Check If `PATH` Set Up Correctly

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

#### Bypass the notarization requirement on macOS

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

#### Instantiate Chrome and Firefox Sessions In Python

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

#### Run Test

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
$ python3 main.py FuncTests.test_delete_instance
```

## Troubleshooting

* `Delete` button not clickable with `click()`: 
  1. There are a few cases in the test where we need to delete a component of the MiniSLATE cluster, such as delete an instance, delete a group and delete a secret.
  2. Interacting with the `Delete` button with invoke a confirmation popup box. During the development, using the `click()` function from Selenium on the `Delete` buttons instead of the `submit()` function is a good way to avoid unexpected errors.
  3. For example, in the Groups Profile page(`groups_profile_template.html` and `groups_profile_secrets.html`), both the `Delete Group` and `Delete Secret` buttons are embeded inside the `<form>` tag in the html. To identify the buttons from the `html`, I used the `find_element_by_xpath()` function from Selenium.
  4. For the `Delete Group` button, I used `.find_element_by_xpath("//div[@aria-label='second group']/form[1]")` to get the button, it was working as expected with the `click()`.
  5. However, when I tried the same thing to get the `Delete Secret` button, the return `<form>` element cannot be interacted with `click()`. It can only be interacted with `submit()`, which caused a problem because the popup confirmation alert that the `submit()` function invokes will lead to a error page when Selenium tries to `.alert.accept()` the confirmation.
  6. A fix to this is to modified the xpath a level deeper passing the `<form>` tag to find the `Delete Secret` button, i.e. `.find_element_by_xpath("//div[@id='{}']/div[1]/form[1]/button[1]".format(secret_field))`. This will return the element as a button so that `click()` can function normally.
