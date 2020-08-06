import unittest
from selenium.webdriver import Chrome
import page
import time


class PortalBrowsing(unittest.TestCase):
    def setUp(self):
        self.driver = Chrome('/opt/WebDriver/bin/chromedriver')
        self.driver.get('https://portal.slateci.io/slate_portal')
    
    def test_check_app_pages(self):
        main_page = page.MainPage(self.driver)
        main_page.go_to_apps_page()
        assert main_page.is_page_valid()
        # print('11111', main_page.get_page_source())
        apps_page = page.AppsPage(self.driver)
        assert apps_page.is_page_valid()

        # get tabs
        stable_apps_text = 'Stable Applications'
        stable_apps_tab = apps_page.driver.find_element_by_link_text(stable_apps_text)
        print(stable_apps_tab.get_attribute('class'))

        incubator_apps_text = 'Incubator Applications'
        incubator_apps_tab = apps_page.driver.find_element_by_link_text(incubator_apps_text)
        print(incubator_apps_tab.get_attribute('class'))
        
        page_number = 1
        click_next = True
        while click_next:
            app_links = apps_page.get_app_links_on_cur_page()
            number_of_links = len(app_links)

            for i in range(number_of_links):
                print('Testing app page:', app_links[i].text)
                app_links[i].click()
                app_detail_page = page.AppDetailPage(self.driver)
                assert app_detail_page.is_page_valid()
                self.driver.back()

                apps_page.wait_until_apps_table_loaded()
                # make sure on the right apps page
                cur_display_page_num = apps_page.get_cur_display_page_num()
                if cur_display_page_num != page_number:
                    apps_page.click_to_page(page_number)
                
                app_links = apps_page.get_app_links_on_cur_page()
            
            next_button = apps_page.get_next_button()
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