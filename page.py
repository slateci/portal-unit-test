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
    def wait_until_apps_table_loaded(self, tab_name):
        next_btn_id = 'apps-table_next'
        if tab_name == 'Incubator Applications':
            next_btn_id = 'incubator-apps-table_next'
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, next_btn_id))
        )
        
    def get_app_links_on_cur_page(self, tab_name):
        # self.wait_until_apps_table_loaded(tab_name)
        table_id = 'apps-table'
        if tab_name == 'Incubator Applications':
            table_id = 'incubator-apps-table'
        apps_table = self.driver.find_element_by_id(table_id)
        app_links = apps_table.find_elements_by_tag_name('a')
        return app_links
    
    def click_cur_page(self, tab_name, page_number):
        pages_id = 'apps-table_paginate'
        if tab_name == 'Incubator Applications':
            pages_id = 'incubator-apps-table_paginate'
        pages = self.driver.find_element_by_id(pages_id)
        # page_to_click = pages.find_element_by_link_text(str(page_number))
        page_to_click = WebDriverWait(pages, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(page_number)))
        )
        if not page_to_click.is_selected():
            page_to_click.click()

    def get_next_button(self, tab_name):
        next_btn_id = 'apps-table_next'
        if tab_name == 'Incubator Applications':
            next_btn_id = 'incubator-apps-table_next'
        return self.driver.find_element_by_id(next_btn_id)

    def get_stable_apps_tab(self):
        return self.driver.find_element_by_link_text('Stable Applications')

    def get_inbubator_apps_tab(self):
        return self.driver.find_element_by_link_text('Incubator Applications')
    
    def click_incubator_apps_tab(self):
        incubator_tab = self.get_inbubator_apps_tab()
        if not incubator_tab.is_selected():
            incubator_tab.click()



class AppDetailPage(BasePage):  
    pass  


class SearchResultPage(BasePage):
    def is_results_found(self):
        return 'No results found.' not in self.driver.page_source