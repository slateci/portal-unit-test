from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locator import *
from element import BasePageElement


class SearchTextElement(BasePageElement):
    locator = 'q'


class BasePage():
    def __init__(self, driver):
        self.driver = driver
    
    def get_page_title(self):
        page_title = self.driver.title
        return page_title
    
    def get_page_source(self):
        return self.driver.page_source

    def is_page_valid(self):
        page_source = self.driver.page_source
        return 'container-error-404' not in page_source or 'container-error-500' not in page_source


class MainPage(BasePage):
    search_text_element = SearchTextElement()

    def is_title_matches(self):
        return 'SLATE - Portal' in self.driver.title
    
    def go_to_apps_page(self):
        button = self.driver.find_element(*MainPageLocators.VIEW_ALL_APPS_BTN)
        button.click()

    def is_apps_link_button_same(self):
        link = self.driver.find_element(*MainPageLocators.APPS_LINK)
        link.click()
        link_dest = self.driver.title
        self.driver.back()
        button = self.driver.find_element(*MainPageLocators.VIEW_ALL_APPS_BTN)
        button.click()
        button_dest = self.driver.title
        return link_dest == button_dest


class AppsPage(BasePage):
    def wait_until_apps_table_loaded(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "apps-table_next"))
        )
        
    def get_app_links_on_cur_page(self):
        self.wait_until_apps_table_loaded()
        apps_table = self.driver.find_element_by_id('apps-table')
        app_links = apps_table.find_elements_by_tag_name('a')
        return app_links
    
    def get_cur_display_page_num(self):
        self.wait_until_apps_table_loaded()
        pages = self.driver.find_element_by_id('apps-table_paginate')
        cur_display_page = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='paginate_button page-item active']"))
        )
        return int(cur_display_page.text)
    
    def click_to_page(self, page_number):
        pages = self.driver.find_element_by_id('apps-table_paginate')
        click_to_page = pages.find_element_by_link_text(str(page_number))
        click_to_page.click()

    def get_next_button(self):
        return self.driver.find_element_by_id('apps-table_next')

    def get_stable_apps_tab(self):
        return self.driver.find_element_by_link_text('Stable Applications')

    def get_inbubator_apps_tab(self):
        return self.driver.find_element_by_link_text('Incubator Applications')


class AppDetailPage(BasePage):  
    pass  


class SearchResultPage(BasePage):
    def is_results_found(self):
        return 'No results found.' not in self.driver.page_source