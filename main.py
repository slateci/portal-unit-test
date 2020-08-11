import unittest
from selenium.webdriver import Chrome, Firefox
import page
import time
import sys


class PortalBrowsing(unittest.TestCase):
    def setUp(self):
        # self.driver = Chrome('/opt/WebDriver/bin/chromedriver')
        self.driver = Firefox('/opt/WebDriver/bin/')
        self.driver.get('https://portal.slateci.io/slate_portal')
    
    def test_check_app_pages(self):
        main_page = page.MainPage(self.driver)
        main_page.go_to_apps_page()
        assert main_page.is_page_valid()
        # print('11111', main_page.get_page_source())
        apps_page = page.AppsPage(self.driver)
        assert apps_page.is_page_valid()
        
        # tab_name = 'Stable Applications'
        # tab_name = 'Incubator Applications'

        for tab_name in ['Stable Applications', 'Incubator Applications']:
            page_number = 1
            click_next = True
            if tab_name == 'Incubator Applications':
                apps_page.click_incubator_apps_tab()
                # here wait till table loaded
                time.sleep(2)

            while click_next:
                apps_page.wait_until_apps_table_loaded(tab_name)
                app_links = apps_page.get_app_links_on_cur_page(tab_name)
                number_of_links = len(app_links)

                print('page number', page_number)

                for i in range(number_of_links):
                    print('Testing app page:', app_links[i].text)
                    app_links[i].click()
                    app_detail_page = page.AppDetailPage(self.driver)
                    assert app_detail_page.is_page_valid()
                    self.driver.back()

                    if tab_name == 'Incubator Applications':
                        apps_page.click_incubator_apps_tab()

                    apps_page.wait_until_apps_table_loaded(tab_name)

                    # make sure on the right apps page
                    apps_page.click_cur_page(tab_name, page_number)
                    
                    apps_page.wait_until_apps_table_loaded(tab_name)
                    app_links = apps_page.get_app_links_on_cur_page(tab_name)
                
                next_button = apps_page.get_next_button(tab_name)
                if next_button.get_attribute('class').split()[-1] == 'disabled':
                    click_next = False
                else:
                    next_button.click()
                    page_number += 1


    def tearDown(self):
        time.sleep(5)
        self.driver.close()


if __name__ == '__main__':
    unittest.main()