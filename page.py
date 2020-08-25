from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
        return 'container-error-404' not in page_source and 'container-error-500' not in page_source and 'Python Stacktrace:' not in page_source
    
    def click_back_btn(self):
        self.driver.back()

class BasePageLoggedIn(BasePage):
    pass

class DashboardPage(BasePage):
    search_text_element = SearchTextElement()

    def is_title_matches(self):
        return 'SLATE - Portal' in self.driver.title
    
    def go_to_clusters_page(self):
        clusters_button = self.driver.find_element(*DashboardPageLocators.CLUSTERS_SIDE_BTN)
        clusters_button.click()
    
    def go_to_apps_page(self):
        apps_button = self.driver.find_element(*DashboardPageLocators.APPS_SIDE_BTN)
        apps_button.click()
    
    def go_to_secrets_page(self):
        secrets_button = self.driver.find_element(*DashboardPageLocators.SECRETS_SIDE_BTN)
        secrets_button.click()
    
    def go_to_instances_page(self):
        instances_button = self.driver.find_element(*DashboardPageLocators.INSTANCES_SIDE_BTN)
        instances_button.click()

    def go_to_my_groups_page(self):
        my_groups_button = self.driver.find_element(*DashboardPageLocators.MY_GROUPS_SIDE_BTN)
        my_groups_button.click()
    
    def go_to_all_groups_page(self):
        all_groups_button = self.driver.find_element(*DashboardPageLocators.ALL_GROUPS_SIDE_BTN)
        all_groups_button.click()
    
    def go_to_cli_access_page(self):
        cli_access_button = self.driver.find_element(*DashboardPageLocators.CLI_ACCESS_SIDE_BTN)
        cli_access_button.click()

    # def is_apps_link_button_same(self):
    #     link = self.driver.find_element(*DashboardPageLocators.APPS_LINK)
    #     link.click()
    #     link_dest = self.driver.title
    #     self.driver.back()
    #     button = self.driver.find_element(*DashboardPageLocators.VIEW_ALL_APPS_BTN)
    #     button.click()
    #     button_dest = self.driver.title
    #     return link_dest == button_dest


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
        return self.driver.find_element(*AppsPageLocators.STABLE_APPS_TAB)
        # return self.driver.find_element_by_link_text('Stable Applications')

    def get_inbubator_apps_tab(self):
        return self.driver.find_element(*AppsPageLocators.INCUBATOR_APPS_TAB)
        # return self.driver.find_element_by_link_text('Incubator Applications')
    
    def click_incubator_apps_tab(self):
        incubator_tab = self.get_inbubator_apps_tab()
        if not incubator_tab.is_selected():
            incubator_tab.click()



class AppDetailPage(BasePage):  
    pass


class ClustersPage(BasePage):
    def wait_until_clusters_table_loaded(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'cluster-table_next'))
        )

    def get_clusters_links_on_cur_page(self):
        clusters_table = self.driver.find_element_by_id('cluster-table')
        clusters_links = clusters_table.find_elements_by_tag_name('a')
        return clusters_links

    def click_cur_page(self, page_number):
        pages = self.driver.find_element_by_id('cluster-table_paginate')
        page_to_click = WebDriverWait(pages, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(page_number)))
        )
        if not page_to_click.is_selected():
            page_to_click.click()

    def get_next_button(self):
        return self.driver.find_element_by_id('cluster-table_next')


class ClusterProfilePage(BasePage):
    pass


class SecretsPage(BasePage):
    def wait_until_secrets_table_loaded(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'secrets-table_next'))
        )

    def get_secret_links_on_cur_page(self):
        pass

    def click_cur_page(self, page_number):
        pass

    def get_next_button(self):
        pass


class SecretGroupPage(BasePage):
    pass


class InstancesPage(BasePage):
    def wait_until_instances_table_loaded(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'instance-table_next'))
        )

    def get_instance_links_on_cur_page(self):
        instances_table = self.driver.find_element_by_id('instance-table')
        instance_links = instances_table.find_elements_by_tag_name('a')
        return instance_links

    def click_cur_page(self, page_number):
        pages = self.driver.find_element_by_id('instance-table_paginate')
        page_to_click = WebDriverWait(pages, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(page_number)))
        )
        if not page_to_click.is_selected():
            page_to_click.click()

    def get_next_button(self):
        return self.driver.find_element_by_id('instance-table_next')


class InstanceProfilePage(BasePage):
    def get_instance_name(self):
        instance_name = self.driver.find_element_by_xpath("//div[@class='col-lg-12 mx-auto']/h2[1]")
        return instance_name.text.split()[-1]

    def get_cluster_name(self):
        cluster_name = self.driver.find_element_by_xpath("//div[@class='col-lg-12 mx-auto']/h6[4]")
        return cluster_name.text.split()[-1]
    
    def get_group_name(self):
        group_name = self.driver.find_element_by_xpath("//div[@class='col-lg-12 mx-auto']/h6[5]")
        return group_name.text.split()[-1]
    
    def get_delete_button(self):
        delete_button = self.driver.find_element_by_link_text('Delete Instance')
        return delete_button
    
    def switch_to_alert_popup(self):
        return self.driver.switch_to.alert
    

class GroupsPage(BasePage):
    def wait_until_groups_table_loaded(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'groups-table_next'))
        )
    
    def get_group_links_on_cur_page(self):
        groups_table = self.driver.find_element_by_id('groups-table')
        group_links = groups_table.find_elements_by_tag_name('a')
        return group_links

    def click_cur_page(self, page_number):
        pages = self.driver.find_element_by_id('groups-table_paginate')
        page_to_click = WebDriverWait(pages, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(page_number)))
        )
        if not page_to_click.is_selected():
            page_to_click.click()

    def get_next_button(self):
        return self.driver.find_element_by_id('groups-table_next')


class MyGroupsPage(GroupsPage):
    def get_register_new_group_btn(self):
        return self.driver.find_element_by_link_text('Register New Group')


class CreateNewGroupPage(BasePage):
    def wait_until_form_loaded(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'cli-access')))

    def fill_group_name(self, group_name):
        group_name_field = self.driver.find_element_by_id('name')
        group_name_field.send_keys(group_name)
    
    def fill_phone_number(self, phone_number):
        phone_number_field = self.driver.find_element_by_id('phone-number')
        phone_number_field.send_keys(phone_number)
    
    def fill_email(self, email):
        email_field = self.driver.find_element_by_id('email')
        email_field.send_keys(email)

    def fill_field_of_science(self, field_of_science):
        field = self.driver.find_element_by_id('field-of-science')
        field.send_keys(field_of_science)
    
    def fill_description(self, description):
        description_field = self.driver.find_element_by_id('description')
        description_field.send_keys(description)
    
    def create_group(self):
        create_btn = self.driver.find_element_by_xpath("//button[@type='submit'][@class='btn btn-primary']")
        create_btn.click()

class GroupProfilePage(BasePage):
    pass


class CLIAccessPage(BasePage):
    pass


class SearchResultPage(BasePage):
    def is_results_found(self):
        return 'No results found.' not in self.driver.page_source