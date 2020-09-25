from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from locator import *
from element import BasePageElement
import os

# class SearchTextElement(BasePageElement):
#     locator = 'q'


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

    def go_to_clusters_page(self):
        clusters_button = self.driver.find_element(*BasePageLocators.CLUSTERS_SIDE_BTN)
        clusters_button.click()
    
    def go_to_apps_page(self):
        apps_button = self.driver.find_element(*BasePageLocators.APPS_SIDE_BTN)
        apps_button.click()
    
    def go_to_secrets_page(self):
        secrets_button = self.driver.find_element(*BasePageLocators.SECRETS_SIDE_BTN)
        secrets_button.click()
    
    def go_to_instances_page(self):
        instances_button = self.driver.find_element(*BasePageLocators.INSTANCES_SIDE_BTN)
        instances_button.click()

    def go_to_my_groups_page(self):
        my_groups_button = self.driver.find_element(*BasePageLocators.MY_GROUPS_SIDE_BTN)
        my_groups_button.click()
    
    def go_to_all_groups_page(self):
        all_groups_button = self.driver.find_element(*BasePageLocators.ALL_GROUPS_SIDE_BTN)
        all_groups_button.click()
    
    def go_to_cli_access_page(self):
        cli_access_button = self.driver.find_element(*BasePageLocators.CLI_ACCESS_SIDE_BTN)
        cli_access_button.click()


class BasePageLoggedIn(BasePage):
    pass

class DashboardPage(BasePage):
    # search_text_element = SearchTextElement()
    def is_title_matches(self):
        return 'SLATE - Portal' in self.driver.title


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
        page_to_click = WebDriverWait(pages, 20).until(
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

    def get_inbubator_apps_tab(self):
        return self.driver.find_element(*AppsPageLocators.INCUBATOR_APPS_TAB)
    
    def click_incubator_apps_tab(self):
        incubator_tab = self.get_inbubator_apps_tab()
        if not incubator_tab.is_selected():
            incubator_tab.click()

    
    def get_app_link(self, app_name): # for app install
        page_number = 1
        click_next = True
        while click_next:
            self.wait_until_apps_table_loaded('Stable Applications')
            apps_table = self.driver.find_element_by_id('apps-table')
            try:
                app_link = apps_table.find_element_by_link_text(app_name)
                click_next = False
                return app_link
            except:
                next_button = self.get_next_button('Stable Applications')
                if next_button.get_attribute('class').split()[-1] == 'disabled':
                    click_next = False
                else:
                    next_button.click()
                    page_number += 1
        return None


class AppsDetailPage(BasePage):  
    def wait_until_ready_for_install(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'app_readme'))
        )
    
    def click_intall_app(self):
        self.driver.find_element(*AppsDetailPageLocators.INSTALL_APP_BTN).click()


class AppCreatePage(BasePage):
    def fill_group(self, group_name='my-group'):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='group']/option[@value='{}']".format(group_name)))
        )
        select = Select(self.driver.find_element_by_id('group'))
        select.select_by_value(group_name)
    
    def get_group_field(self):
        return self.driver.find_element_by_id('group')
    
    def click_next(self):
        self.driver.find_element(*AppCreatePageLocators.NEXT_BTN).click()


class AppCreateFinalPage(BasePage):
    def fill_cluster(self, cluster_name='my-cluster'):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='cluster']/option[@value='{}']".format(cluster_name)))
        )
        select = Select(self.driver.find_element_by_id('cluster'))
        select.select_by_value(cluster_name)
    
    def get_cluster_field(self):
        return self.driver.find_element_by_id('cluster')

    def fill_configuration(self, app_suffix=''):
        conf_field = self.driver.find_element_by_id('config')
        # print(conf_field.text)
        config_arr = conf_field.text.split('\n')
        # add suffix to app name
        for idx, line in enumerate(config_arr):
            if 'Instance:' in line:
                config_arr[idx] = "Instance: {}".format(app_suffix)
                break      
        conf_field.clear()
        conf_field.send_keys('\n'.join(config_arr))
        # print('\n'.join(config_arr))

    def click_install(self):
        self.driver.find_element(*AppCreateFinalPageLocators.INSTALL_BTN).click()


class ClustersPage(BasePage):
    def wait_until_clusters_table_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'cluster-table_next'))
        )

    def get_clusters_links_on_cur_page(self):
        clusters_table = self.driver.find_element_by_id('cluster-table')
        clusters_links = clusters_table.find_elements_by_tag_name('a')
        return clusters_links

    def click_cur_page(self, page_number):
        pages = self.driver.find_element_by_id('cluster-table_paginate')
        page_to_click = WebDriverWait(pages, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(page_number)))
        )
        if not page_to_click.is_selected():
            page_to_click.click()

    def get_next_button(self):
        return self.driver.find_element_by_id('cluster-table_next')


class ClusterPublicProfilePage(BasePage):
    pass


class ClusterProfilePage(BasePage):
    def wait_until_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'cluster-profile'))
        )

    def get_edit_info_btn(self):
        return self.driver.find_element_by_link_text('Edit Info')

    def get_group_selector(self):
        return self.driver.find_element_by_id('new_group')
    
    def set_group_selector(self, group_name):
        selector = self.get_group_selector()
        selector.send_keys(group_name)

    def get_add_group_btn(self, cluster_name):
        return self.driver.find_element_by_xpath("//form[@action='/groups/my-group/clusters/{}']/button[1]".format(cluster_name))

    def get_revoke_btn(self, group_to_revoke):
        return self.driver.find_element_by_xpath("//button[@name='remove_group'][@value='{}']".format(group_to_revoke))
    
    def get_added_group_link(self, group_name, cluster_name, group_added):
        try:
            return self.driver.find_element_by_xpath("//a[@href='/groups/{}/clusters/{}/{}']".format(group_name, cluster_name, group_added))
        except:
            return None

class ClusterEditPage(BasePage):
    def wait_until_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//form[@role='form']"))
        )
    
    def get_org_field(self):
        return self.driver.find_element_by_id('owningOrganization')

    def set_org_field(self, org_name):
        org_field = self.get_org_field()
        org_field.clear()
        org_field.send_keys(org_name)

    def get_latitude_field(self):
        return self.driver.find_element_by_id('latitude')

    def set_latitude_field(self, latitude):
        lat_field = self.get_latitude_field()
        lat_field.clear()
        lat_field.send_keys(latitude)

    def get_longitude_field(self):
        return self.driver.find_element_by_id('longitude')

    def set_longitude_field(self, longitude):
        long_field = self.get_longitude_field()
        long_field.clear()
        long_field.send_keys(longitude)

    def get_update_btn(self):
        return self.driver.find_element_by_xpath("//button[@class='btn btn-primary']")



class SecretsPage(BasePage):
    def wait_until_secrets_table_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'secrets-table_next'))
        )

    def get_secret_links_on_cur_page(self):
        secrets_links = self.driver.find_elements_by_xpath("//td[@class='sorting_1']/a[1]")
        return secrets_links

    def click_cur_page(self, page_number):
        pages = self.driver.find_element_by_id('secrets-table_paginate')
        page_to_click = WebDriverWait(pages, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(page_number)))
        )
        if not page_to_click.is_selected():
            page_to_click.click()

    def get_next_button(self):
        return self.driver.find_element_by_id('secrets-table_next')


class SecretGroupPage(BasePage):
    pass

class SecretsCreatePage(BasePage):
    # use implicit wait instead
    # def wait_until_form_loaded(self):
    #     WebDriverWait(self.driver, 20).until(
    #         EC.presence_of_element_located((By.LINK_TEXT, 'Add Secret'))
    #     )

    def get_cluster_field(self):
        return self.driver.find_element_by_id('cluster')

    def select_cluster(self, cluster_name):
        cluster_field = self.driver.find_element_by_id('cluster')
        cluster_field.send_keys(cluster_name)
    
    def get_secret_name_field(self):
        return self.driver.find_element_by_id('secret_name')

    def fill_secret_name(self, secret_name):
        secret_name_field = self.driver.find_element_by_id('secret_name')
        secret_name_field.clear()
        secret_name_field.send_keys(secret_name)

    def get_key_name_field(self):
        return self.driver.find_element_by_id('key_name')

    def fill_key_name(self, key_name):
        key_name_field = self.driver.find_element_by_id('key_name')
        key_name_field.clear()
        key_name_field.send_keys(key_name)

    def fill_key_contents(self, key_contents):
        key_contents_field = self.driver.find_element_by_id('key_contents')
        key_contents_field.clear()
        key_contents_field.send_keys(key_contents)

    def get_add_key_contents_btn(self):
        pass

    def get_add_secret_btn(self):
        return self.driver.find_element_by_xpath("//button[@type='submit'][@class='btn btn-primary']")
    
    def fill_form_and_submit(self, cluster_name, secret_name, key_name, key_contents):
        self.driver.implicitly_wait(5)
        self.select_cluster(cluster_name)
        self.fill_secret_name(secret_name)
        self.fill_key_name(key_name)
        self.fill_key_contents(key_contents)
        self.get_add_secret_btn().click()


class InstancesPage(BasePage):
    def wait_until_instances_table_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'instance-table_next'))
        )

    def get_instance_links_on_cur_page(self):
        instances_table = self.driver.find_element_by_id('instance-table')
        instance_links = instances_table.find_elements_by_tag_name('a')
        return instance_links

    def click_cur_page(self, page_number):
        pages = self.driver.find_element_by_id('instance-table_paginate')
        page_to_click = WebDriverWait(pages, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, str(page_number)))
        )
        if not page_to_click.is_selected():
            page_to_click.click()

    def get_next_button(self):
        return self.driver.find_element_by_id('instance-table_next')
    
    def get_instance_link(self, instance_name):
        page_number = 1
        click_next = True
        while click_next:
            self.wait_until_instances_table_loaded()
            instances_table = self.driver.find_element_by_id('instance-table')
            try:
                instance_link = instances_table.find_element_by_link_text(instance_name)
                click_next = False
                return instance_link
            except:
                next_button = self.get_next_button()
                if next_button.get_attribute('class').split()[-1] == 'disabled':
                    click_next = False
                else:
                    next_button.click()
                    page_number += 1
        return None


class InstanceProfilePage(BasePage):
    def wait_until_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'details'))
        )
    def get_instance_name(self):
        instance_name = self.driver.find_element_by_xpath("//div[@class='col-lg-12 mx-auto']/h2[1]")
        return instance_name.text.split()[-1]

    def get_app_name(self):
        app_name = self.driver.find_element_by_xpath("//div[@class='col-lg-12 mx-auto']/h6[2]")
        return app_name.text.split()[-1]

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
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'groups-table_next'))
        )
    
    def get_group_links_on_cur_page(self):
        groups_table = self.driver.find_element_by_id('groups-table')
        group_links = groups_table.find_elements_by_tag_name('a')
        return group_links

    def get_group_link(self, group_name):
        page_number = 1
        click_next = True
        while click_next:
            self.wait_until_groups_table_loaded()
            groups_table = self.driver.find_element_by_id('groups-table')
            try:
                group_link = groups_table.find_element_by_link_text(group_name)
                click_next = False
                return group_link
            except:
                next_button = self.get_next_button()
                if next_button.get_attribute('class').split()[-1] == 'disabled':
                    click_next = False
                else:
                    next_button.click()
                    page_number += 1
        return None

    def get_group_link_2(self, group_name):
        groups_table = self.driver.find_element_by_id('groups-table')
        group = groups_table.find_element_by_link_text(group_name)
        return group

    def click_cur_page(self, page_number):
        pages = self.driver.find_element_by_id('groups-table_paginate')
        page_to_click = WebDriverWait(pages, 20).until(
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
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'cli-access')))

    def get_group_name_field(self):
        return self.driver.find_element_by_id('name')

    def fill_group_name(self, group_name):
        group_name_field = self.driver.find_element_by_id('name')
        group_name_field.clear()
        group_name_field.send_keys(group_name)
    
    def get_phone_number_field(self):
        return self.driver.find_element_by_id('phone-number')

    def fill_phone_number(self, phone_number):
        phone_number_field = self.driver.find_element_by_id('phone-number')
        phone_number_field.clear()
        phone_number_field.send_keys(phone_number)
    
    def get_email_field(self):
        return self.driver.find_element_by_id('email')
    
    def fill_email(self, email):
        email_field = self.driver.find_element_by_id('email')
        email_field.clear()
        email_field.send_keys(email)

    def get_field_of_science(self):
        return self.driver.find_element_by_id('field-of-science')


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
    def wait_until_page_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'accessible-clusters-table_next')))
    
    def get_group_name(self):
        group_name = self.driver.find_element_by_xpath("//div[@id='group-info']/span[1]/h2[1]")
        return group_name.text.split()[-1]
    
    def get_description(self):
        description = self.driver.find_element_by_xpath("//div[@id='group-info']/span[1]/p[1]")
        return description.text

    def get_field_of_science(self):
        field_of_science = self.driver.find_element_by_xpath("//div[@id='group-info']/span[1]/p[2]")
        return field_of_science.text.split()[-1]

    def get_email(self):
        email = self.driver.find_element_by_xpath("//div[@id='group-info']/span[1]/p[3]")
        return email.text.split()[-1]

    def get_phone_number(self):
        phone_number = self.driver.find_element_by_xpath("//div[@id='group-info']/span[1]/p[4]")
        return phone_number.text.split()[-1]

    def get_edit_btn(self):
        return self.driver.find_element_by_link_text('Edit Info') 

    def get_delete_group_btn(self):
        return self.driver.find_element_by_xpath("//div[@aria-label='second group']/form[1]")

    def switch_to_alert_popup(self):
        return self.driver.switch_to.alert
    
    def get_cluster_link(self, cluster_name):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'table-data'))
            )
        try:
            link = self.driver.find_element_by_link_text(cluster_name)
            return link
        except:
            return None
    
    def get_secrets_tab(self):
        return self.driver.find_element_by_id('secrets_tab')

    def get_new_secret_btn(self):
        new_secret_btn = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//form[@role='form'][@action='/groups/my-group/new_secret']"))
            )
        return new_secret_btn

    def get_secret_link(self, created_secret):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'secrets-vue'))
            )
        try:
            link = self.driver.find_element_by_link_text(created_secret)
            return link
        except:
            return None

    def get_secret_link_delete_btn(self, group_name, secret_field):
        content_field = secret_field + '-contents'
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.ID, content_field))
            )
        
        return self.driver.find_element_by_xpath("//div[@id='{}']/div[1]/form[1]/button[1]".format(secret_field))



class GroupEditPage(BasePage):
    def wait_until_form_loaded(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'cli-access')))
    
    def get_email_field(self):
        return self.driver.find_element_by_id('email')
    
    def update_email(self, email):
        email_field = self.driver.find_element_by_id('email')
        email_field.clear()
        email_field.send_keys(email)

    def get_phone_number_field(self):
        return self.driver.find_element_by_id('phone-number')
    
    def update_phone_number(self, phone_number):
        phone_number_field = self.driver.find_element_by_id('phone-number')
        phone_number_field.clear()
        phone_number_field.send_keys(phone_number)
    
    def get_science_field(self):
        return self.driver.find_element_by_id('field-of-science')

    def update_field_of_science(self, field_of_science):
        field_sc = self.driver.find_element_by_id('field-of-science')
        field_sc.send_keys(field_of_science)
    
    def update_description(self, description):
        description_field = self.driver.find_element_by_id('description')
        description_field.clear()
        description_field.send_keys(description)
    
    def update_group(self):
        update_btn = self.driver.find_element_by_xpath("//button[@type='submit'][@class='btn btn-primary btn-box-shadow']")
        update_btn.click()

class CLIAccessPage(BasePage):
    pass


class SearchResultPage(BasePage):
    def is_results_found(self):
        return 'No results found.' not in self.driver.page_source