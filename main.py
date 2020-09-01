import unittest
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import page
import time
# import os


class PortalBrowsing(unittest.TestCase):
    def setUp(self):
        # test with Firefox, without headless()
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver')
        # test with Firefox, with headless()
        # options = FirefoxOptions()
        # options.headless = True
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver', options=options)

        # test with chrome, without headless()
        # self.driver = Chrome('/opt/WebDriver/bin/chromedriver')
        # test with chrome, with headless()
        options = ChromeOptions()
        options.headless = True
        # options.headless = False
        self.driver = Chrome(executable_path='/opt/WebDriver/bin/chromedriver', options=options)

        # portal on minislate
        self.driver.get('http://localhost:5000/slate_portal')
        # slate portal
        # self.driver.get('https://portal.slateci.io/slate_portal')
        self.driver.set_window_size(1920, 1080)


    def test_iterate_clusters_pages(self):
        clusters_page = self.segue_to_page('clusters')
        page_number = 1
        click_next = True

        while click_next:
            clusters_page.wait_until_clusters_table_loaded()
            clusters_links = clusters_page.get_clusters_links_on_cur_page()
            num_of_links = len(clusters_links)

            print('page number', page_number)

            for i in range(num_of_links):
                print('Testing cluster page:', clusters_links[i].text)
                clusters_links[i].click()
                clusters_profile_page = page.ClusterProfilePage(self.driver)
                assert clusters_profile_page.is_page_valid()
                self.driver.back()
                clusters_page.wait_until_clusters_table_loaded()
                clusters_page.click_cur_page(page_number)
                clusters_page.wait_until_clusters_table_loaded()
                clusters_links = clusters_page.get_clusters_links_on_cur_page()

            next_button = clusters_page.get_next_button()
            if next_button.get_attribute('class').split()[-1] == 'disabled':
                click_next = False
            else:
                next_button.click()
                page_number += 1


    def test_iterate_apps_pages(self):
        apps_page = self.segue_to_page('applications')

        for tab_name in ['Stable Applications', 'Incubator Applications']:
            page_number = 1
            click_next = True
            if tab_name == 'Incubator Applications':
                apps_page.click_incubator_apps_tab()
                self.driver.implicitly_wait(3) # implicitly waiting for Incubator Applications tab loaded

            while click_next:
                apps_page.wait_until_apps_table_loaded(tab_name)
                app_links = apps_page.get_app_links_on_cur_page(tab_name)
                number_of_links = len(app_links)

                print('page number', page_number)

                for i in range(number_of_links):
                    print('Testing app page:', app_links[i].text)
                    app_links[i].click()
                    app_detail_page = page.AppsDetailPage(self.driver)
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

    def test_iterate_instances_pages(self):
        instances_page = self.segue_to_page('instances')

        page_number = 1
        click_next = True

        while click_next:
            instances_page.wait_until_instances_table_loaded()
            instance_links = instances_page.get_instance_links_on_cur_page()
            num_of_links = len(instance_links)

            print('page number', page_number)

            for i in range(num_of_links):
                print('Testing instance page:', instance_links[i].text)
                instance_links[i].click()
                instance_detail_page = page.InstanceProfilePage(self.driver)
                assert instance_detail_page.is_page_valid()
                self.driver.back()
                instances_page.wait_until_instances_table_loaded()
                instances_page.click_cur_page(page_number)
                instances_page.wait_until_instances_table_loaded()
                instance_links = instances_page.get_instance_links_on_cur_page()

            next_button = instances_page.get_next_button()
            if next_button.get_attribute('class').split()[-1] == 'disabled':
                click_next = False
            else:
                next_button.click()
                page_number += 1


    def test_iterate_my_groups_pages(self):
        my_groups_page = self.segue_to_page('my_groups')
        page_number = 1
        click_next = True

        while click_next:
            my_groups_page.wait_until_groups_table_loaded()
            my_groups_links = my_groups_page.get_group_links_on_cur_page()
            num_of_links = len(my_groups_links)

            print('page number', page_number)

            for i in range(num_of_links):
                print('Testing group page:', my_groups_links[i].text)
                my_groups_links[i].click()
                my_groups_detail_page = page.GroupProfilePage(self.driver)
                assert my_groups_detail_page.is_page_valid()
                self.driver.back()
                my_groups_page.wait_until_groups_table_loaded()
                my_groups_page.click_cur_page(page_number)
                my_groups_page.wait_until_groups_table_loaded()
                my_groups_links = my_groups_page.get_group_links_on_cur_page()

            next_button = my_groups_page.get_next_button()
            if next_button.get_attribute('class').split()[-1] == 'disabled':
                click_next = False
            else:
                next_button.click()
                page_number += 1
    
    def test_iterate_all_groups_pages(self):
        all_groups_page = self.segue_to_page('all_groups')
        page_number = 1
        click_next = True

        while click_next:
            all_groups_page.wait_until_groups_table_loaded()
            all_groups_links = all_groups_page.get_group_links_on_cur_page()
            num_of_links = len(all_groups_links)

            print('page number', page_number)

            for i in range(num_of_links):
                print('Testing group page:', all_groups_links[i].text)
                all_groups_links[i].click()
                all_groups_detail_page = page.GroupProfilePage(self.driver)
                assert all_groups_detail_page.is_page_valid()
                self.driver.back()
                all_groups_page.wait_until_groups_table_loaded()
                all_groups_page.click_cur_page(page_number)
                all_groups_page.wait_until_groups_table_loaded()
                all_groups_links = all_groups_page.get_group_links_on_cur_page()

            next_button = all_groups_page.get_next_button()
            if next_button.get_attribute('class').split()[-1] == 'disabled':
                click_next = False
            else:
                next_button.click()
                page_number += 1
    
    def test_check_cli_access_page(self):
        self.segue_to_page('cli_access')

    
    def segue_to_page(self, page_name):
        start_page = page.BasePage(self.driver)
        assert start_page.is_page_valid()
        cur_page = None
        if page_name == 'clusters':
            start_page.go_to_clusters_page()
            cur_page = page.ClustersPage(self.driver)
        elif page_name == 'applications':
            start_page.go_to_apps_page()
            cur_page = page.AppsPage(self.driver)
        elif page_name == 'instances':
            start_page.go_to_instances_page()
            cur_page = page.InstancesPage(self.driver)
        elif page_name == 'my_groups':
            start_page.go_to_my_groups_page()
            cur_page = page.MyGroupsPage(self.driver)
        elif page_name == 'all_groups':
            start_page.go_to_all_groups_page()
            cur_page = page.GroupsPage(self.driver)
        elif page_name == 'cli_access':
            start_page.go_to_cli_access_page()
            cur_page = page.CLIAccessPage(self.driver)
        assert cur_page.is_page_valid()
        return cur_page

    def tearDown(self):
        # self.driver.implicitly_wait(3)
        # time.sleep(3)
        self.driver.close()

class FuncTests(unittest.TestCase):
    def setUp(self):
        # test with Firefox, without headless()
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver')
        # test with Firefox, with headless()
        options = FirefoxOptions()
        # options.headless = True
        options.headless = False
        self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver', options=options)

        # test with chrome, without headless()
        # self.driver = Chrome('/opt/WebDriver/bin/chromedriver')
        # test with chrome, with headless()
        # options = ChromeOptions()
        # options.headless = True
        # options.headless = False
        # self.driver = Chrome(executable_path='/opt/WebDriver/bin/chromedriver', options=options)

        # portal on minislate
        self.driver.get('http://localhost:5000/slate_portal')
        # slate portal
        # self.driver.get('https://portal.slateci.io/slate_portal')
        self.driver.set_window_size(1920, 1080)

    def segue_to_page(self, page_name):
        start_page = page.BasePage(self.driver)
        assert start_page.is_page_valid()
        cur_page = None
        if page_name == 'clusters':
            start_page.go_to_clusters_page()
            cur_page = page.ClustersPage(self.driver)
        elif page_name == 'applications':
            start_page.go_to_apps_page()
            cur_page = page.AppsPage(self.driver)
        elif page_name == 'instances':
            start_page.go_to_instances_page()
            cur_page = page.InstancesPage(self.driver)
        elif page_name == 'my_groups':
            start_page.go_to_my_groups_page()
            cur_page = page.MyGroupsPage(self.driver)
        assert cur_page.is_page_valid()
        return cur_page
    

    def test_add_instance(self):
        print('test_add_instance')
        app_name = 'nginx'
        app_suffix = 'test-add'
        instance_detail_page = self.add_instance(app_name, app_suffix=app_suffix)
    

    def add_instance(self, app_name, app_suffix=''):
        apps_page = self.segue_to_page('applications')
        # app_to_install = 'nginx'
        installed = False
        # find the app
        
        instance_detail_page = None
            
        apps_page.wait_until_apps_table_loaded('Stable Applications')
        app_link = apps_page.get_app_link(app_name)

        if app_link:
            print('installing', app_link.text)
            app_link.click()
            app_detail_page = page.AppsDetailPage(self.driver)
            assert app_detail_page.is_page_valid()
            app_detail_page.wait_until_ready_for_install()
            app_detail_page.click_intall_app()
            
            app_create_page = page.AppCreatePage(self.driver)
            assert app_create_page.is_page_valid()
            app_create_page.fill_group()
            app_create_page.click_next()

            app_create_final_page = page.AppCreateFinalPage(self.driver)
            assert app_create_final_page.is_page_valid()
            app_create_final_page.fill_cluster()
            app_create_final_page.fill_configuration(app_suffix)
            app_create_final_page.click_install()

            # enter instance detail page; check instance name
            instance_detail_page = page.InstanceProfilePage(self.driver)
            assert instance_detail_page.is_page_valid()
            instance_detail_page.wait_until_page_loaded()

            installed_app_name = instance_detail_page.get_app_name()
            assert installed_app_name == app_name
            
            # change install flag to true
            installed = True
        
        assert installed
        print('Instance: {} installed'.format(app_name))
        return instance_detail_page


    def test_delete_instance(self):
        print('test_delete_instance')
        # add a new instance for delete
        app_name = 'nginx'
        app_suffix = 'test-delete'
        instance_detail_page = self.add_instance(app_name,app_suffix=app_suffix)
        
        # delete the instance 
        instances_page = self.segue_to_page('instances')
        instances_page.wait_until_instances_table_loaded()
        instance_name = app_name + '-' + app_suffix
        
        instance_link = instances_page.get_instance_link(instance_name)

        instance_link.click()
        instance_detail_page = page.InstanceProfilePage(self.driver)
        assert instance_detail_page.is_page_valid()

        instance_name = instance_detail_page.get_instance_name()
        cluster_name = instance_detail_page.get_cluster_name()
        group_name = instance_detail_page.get_group_name()
        
        print('Click Delete button of {}'.format(instance_name))
        instance_detail_page.get_delete_button().click()
        try:
            alert = instance_detail_page.switch_to_alert_popup()
            # time.sleep(1)
            alert.accept()
            print('Alert pop up accepted')
        except:
            print('Error occur at confirming instance delete')

        # check instance deleted
        instances_page.wait_until_instances_table_loaded()
        instance_link = instances_page.get_instance_link(instance_name)
        assert not instance_link
        print('Instance {} successfully deleted'.format(instance_name))


    def add_group(self, group_name, field_of_science):
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.get_register_new_group_btn().click()
        create_new_group = page.CreateNewGroupPage(self.driver)
        create_new_group.fill_group_name(group_name)
        create_new_group.fill_field_of_science(field_of_science)
        create_new_group.create_group()
        
        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()


    def test_add_group(self):
        print('test_add_new_group')
        group_name = 'test-add-group'
        field_of_science = 'Biology'
        self.add_group(group_name, field_of_science)


    def test_edit_group(self):
        # add group for edit
        group_name = 'test-edit-group'
        field_of_science = 'Biology'
        print('adding group {} for edit group test'.format(group_name))
        self.add_group(group_name, field_of_science)
        # edit group
        print('test_edit_group')
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()
        group_profile_page.wait_until_page_loaded
        group_profile_page.get_edit_btn().click()

        group_edit_page = page.GroupEditPage(self.driver)
        assert group_edit_page.is_page_valid()
        group_edit_page.wait_until_form_loaded()

        new_email = 'selenium-test@slateci.io'
        new_phone_number = '777-7777'
        new_field_of_science = 'Physics'
        new_description = 'Testing group edit functionality'

        group_edit_page.update_email(new_email)
        group_edit_page.update_phone_number(new_phone_number)
        group_edit_page.update_field_of_science(new_field_of_science)
        group_edit_page.update_description(new_description)
        # click update
        group_edit_page.update_group()

        # here should add assert to confirm group info updated
        group_profile_page.wait_until_page_loaded()
        assert group_profile_page.is_page_valid()
        assert group_profile_page.get_field_of_science() == new_field_of_science
        assert group_profile_page.get_email() == new_email
        assert group_profile_page.get_phone_number() == new_phone_number


    def test_delete_group(self):
        # add group for delete
        group_name = 'test-delete-group'
        field_of_science = 'Biology'
        print('adding group {} for delete group test'.format(group_name))
        self.add_group(group_name, field_of_science)
        # delete group
        print('test_delete_group')
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()
        group_profile_page.wait_until_page_loaded
        group_profile_page.get_delete_group_btn().click()
        try:
            alert = group_profile_page.switch_to_alert_popup()
            # time.sleep(1)
            # alert.accept()
            alert.dismiss()
            print('Alert pop up accepted')
        except:
            print('Error occur at confirming group delete')
        
        # confirm group deleted
        group_link = my_groups_page.get_group_link(group_name)
        assert not group_link

    
    def add_secret(self, cluster_name, secret_name, key_name, key_contents):
        group_name = 'my-group'
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()
        group_profile_page.wait_until_page_loaded

        group_profile_page.get_secrets_tab().click()
        group_profile_page.get_new_secret_btn().submit()

        secrets_create_page = page.SecretsCreatePage(self.driver)
        secrets_create_page.fill_form_and_submit(cluster_name, secret_name, key_name, key_contents)


    def test_add_secret(self):
        cluster_name = 'my-cluster'
        secret_name = 'test-secret'
        key_name = 'test-key-name'
        key_contents = 'test-key-contents'
        self.add_secret(cluster_name, secret_name, key_name, key_contents)

        created_secret = '{}: {}'.format(cluster_name, secret_name)
        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()

        created_secret_link = group_profile_page.get_secret_link(created_secret)
        assert created_secret == created_secret_link.text
        created_secret_link.click()

    
    def test_delete_secret(self):
        # first create secret for delete
        group_name = 'my-group'
        cluster_name = 'my-cluster'
        secret_name = 'test-delete-secret'
        key_name = 'test-delete-key-name'
        key_contents = 'test-delete-key-contents'

        self.add_secret(cluster_name, secret_name, key_name, key_contents)
        created_secret = '{}: {}'.format(cluster_name, secret_name)
        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()

        created_secret_link = group_profile_page.get_secret_link(created_secret)
        assert created_secret == created_secret_link.text
        created_secret_link.click() # expand the secret_content_field

        # find the delete button and click()
        secret_field = '{}-{}'.format(cluster_name, secret_name) # 'my-cluster-test-delete-secret'
        secret_delete_btn = group_profile_page.get_secret_link_delete_btn(group_name, secret_field)
        # print('test1', secret_delete_btn[0].text)
        secret_delete_btn.submit()

        try:
            alert = group_profile_page.switch_to_alert_popup()
            # time.sleep(1)
            # alert.accept()
            alert.dimiss()
            print('Alert pop up accepted')
        except:
            print('Error occur at confirming secret delete')

        # confirm deletion
        # created_secret_link = group_profile_page.get_secret_link(created_secret)
        # assert not created_secret_link
    

    def tearDown(self):
        # self.driver.implicitly_wait(3)
        time.sleep(15)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()