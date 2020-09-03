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
        # options.headless = True
        options.headless = False
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


    def test_iterate_secrets_pages(self):
        secrets_page = self.segue_to_page('secrets')
        page_number = 1
        click_next = True
        
        while click_next:
            secrets_page.wait_until_secrets_table_loaded()
            secrets_links = secrets_page.get_secret_links_on_cur_page()
            num_of_links = len(secrets_links)
            print(num_of_links)
            print('page number', page_number)

            for i in range(num_of_links):
                print('Testing secrete page:', secrets_links[i].text)
                secrets_links[i].click()
                group_profile_page = page.GroupProfilePage(self.driver)
                assert group_profile_page.is_page_valid()
                self.driver.back()

                secrets_page.wait_until_secrets_table_loaded()
                secrets_page.click_cur_page(page_number)
                secrets_page.wait_until_secrets_table_loaded()
                secrets_links = secrets_page.get_secret_links_on_cur_page()
            
            next_button = secrets_page.get_next_button()
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
        elif page_name == 'secrets':
            start_page.go_to_secrets_page()
            cur_page = page.SecretsPage(self.driver)
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
        time.sleep(3)
        self.driver.close()

class FuncTests(unittest.TestCase):
    def setUp(self):
        # test with Firefox, without headless()
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver')
        # test with Firefox, with headless()
        # options = FirefoxOptions()
        # options.headless = True
        # options.headless = False
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver', options=options)

        # test with chrome, without headless()
        # self.driver = Chrome('/opt/WebDriver/bin/chromedriver')
        # test with chrome, with headless()
        options = ChromeOptions()
        # options.headless = True
        options.headless = False
        self.driver = Chrome(executable_path='/opt/WebDriver/bin/chromedriver', options=options)

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

    
    def test_add_instance_wrong_input(self):
        print('test add instance with wrong input')
        app_name = 'nginx'
        app_suffix = 'test-add-with-wrong-input'
        apps_page = self.segue_to_page('applications')
        
        apps_page.wait_until_apps_table_loaded('Stable Applications')
        app_link = apps_page.get_app_link(app_name)

        if app_link:
            print('installing', app_link.text)
            app_link.click()
            app_detail_page = page.AppsDetailPage(self.driver)
            assert app_detail_page.is_page_valid()
            app_detail_page.wait_until_ready_for_install()
            app_detail_page.click_intall_app()

            # test missing group name
            app_create_page = page.AppCreatePage(self.driver)
            assert app_create_page.is_page_valid()
            app_create_page.fill_group(group_name='')
            app_create_page.click_next()
            
            group_field = app_create_page.get_group_field()
            message = group_field.get_attribute('validationMessage')
            assert message == 'Please select an item in the list.'

            # select a valid group and proceed to next page
            app_create_page.fill_group()
            app_create_page.click_next()

            # test missing cluster name
            app_create_final_page = page.AppCreateFinalPage(self.driver)
            assert app_create_final_page.is_page_valid()
            app_create_final_page.fill_cluster(cluster_name='')
            app_create_final_page.fill_configuration(app_suffix)
            app_create_final_page.click_install()

            cluster_field = app_create_final_page.get_cluster_field()
            message = cluster_field.get_attribute('validationMessage')
            assert message == 'Please select an item in the list.'

    

    def add_instance(self, app_name, app_suffix=''):
        apps_page = self.segue_to_page('applications')
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


    def add_group(self, group_name='valid-name', phone_number='555-5555', email='slate@slateci.io', field_of_science='Biology'):
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.get_register_new_group_btn().click()
        create_new_group = page.CreateNewGroupPage(self.driver)
        # create_new_group.wait_until_form_loaded()

        create_new_group.fill_group_name(group_name)
        create_new_group.fill_phone_number(phone_number)
        create_new_group.fill_email(email)
        create_new_group.fill_field_of_science(field_of_science)
        create_new_group.create_group()
        
        cur_page = page.BasePage(self.driver)
        assert cur_page.is_page_valid()
    

    def test_add_group(self):
        print('test add new group')
        group_name = 'test-add-group'
        self.add_group(group_name=group_name)
    
    
    def test_add_group_wrong_input(self):
        print('test adding new group with wrong inputs')
        # test invalid group name
        invalid_group_name = 'valid@name'
        self.add_group(group_name=invalid_group_name)
        create_new_group_page = page.CreateNewGroupPage(self.driver)
        group_name_field = create_new_group_page.get_group_name_field()
        message = group_name_field.get_attribute('validationMessage')
        assert message == 'Please match the requested format.'

        # test empty phone number field
        empty_phone_number = ''
        self.add_group(phone_number=empty_phone_number)
        create_new_group_page = page.CreateNewGroupPage(self.driver)
        phone_number_field = create_new_group_page.get_phone_number_field()
        message = phone_number_field.get_attribute('validationMessage')
        assert message == 'Please fill out this field.'

        # test invalid email (without '@')
        invalid_email = 'slate-slateci.io'
        self.add_group(email=invalid_email)
        create_new_group_page = page.CreateNewGroupPage(self.driver)
        email_field = create_new_group_page.get_email_field()
        message = email_field.get_attribute('validationMessage')
        assert message == "Please include an '@' in the email address. '{}' is missing an '@'.".format(invalid_email)

        # test empty field of science
        empty_field_of_science = ''
        self.add_group(field_of_science=empty_field_of_science)
        create_new_group_page = page.CreateNewGroupPage(self.driver)
        science_field = create_new_group_page.get_field_of_science()
        message = science_field.get_attribute('validationMessage')
        assert message == 'Please select an item in the list.'
    

    def test_edit_group_wrong_input(self):
        print('test editing new group with wrong inputs')
        # add group for edit with wrong input
        group_name = 'test-edit-group-wrong-input'
        print('adding group {} for edit group test'.format(group_name))
        self.add_group(group_name=group_name)
        # edit with wrong input
        print('test_edit_group_with_wrong_input')
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()
        group_profile_page.wait_until_page_loaded()
        group_profile_page.get_edit_btn().click()

        group_edit_page = page.GroupEditPage(self.driver)
        assert group_edit_page.is_page_valid()
        group_edit_page.wait_until_form_loaded()

        # test invalid email input
        invalid_email = 'selenium-testslateci.io'
        self.edit_group_on_edit_page(group_edit_page, email=invalid_email)
        email_field = group_edit_page.get_email_field()
        message = email_field.get_attribute('validationMessage')
        assert message == "Please include an '@' in the email address. '{}' is missing an '@'.".format(invalid_email)

        # test missing phone number
        missing_phone_number = ''
        self.edit_group_on_edit_page(group_edit_page, phone_number=missing_phone_number)
        phone_number_field = group_edit_page.get_phone_number_field()
        message = phone_number_field.get_attribute('validationMessage')
        assert message == 'Please fill out this field.'

        # # test empty field of science
        # empty_field_of_science = ''
        # self.edit_group_on_edit_page(group_edit_page, field_of_science=empty_field_of_science)
        # science_field = group_edit_page.get_science_field()
        # message = science_field.get_attribute('validationMessage')
        # print(message)
        

    def edit_group_on_edit_page(self, group_edit_page, email='selenium-test@slateci.io', phone_number='777-7777', field_of_science='Physics', description='Testing group edit functionality'):
        group_edit_page.update_email(email)
        group_edit_page.update_phone_number(phone_number)
        group_edit_page.update_field_of_science(field_of_science)
        group_edit_page.update_description(description)
        # click update
        group_edit_page.update_group()



    def test_edit_group(self):
        # add group for edit
        group_name = 'test-edit-group'
        print('adding group {} for edit group test'.format(group_name))
        self.add_group(group_name=group_name)
        # edit group
        print('test_edit_group')
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()
        group_profile_page.wait_until_page_loaded()
        group_profile_page.get_edit_btn().click()

        group_edit_page = page.GroupEditPage(self.driver)
        assert group_edit_page.is_page_valid()
        group_edit_page.wait_until_form_loaded()

        new_email = 'selenium-test@slateci.io'
        new_phone_number = '777-7777'
        new_field_of_science = 'Physics'
        new_description = 'Testing group edit functionality'
        self.edit_group_on_edit_page(group_edit_page, email=new_email, phone_number=new_phone_number, field_of_science=new_field_of_science, description=new_description)

        # confirm group info updated
        group_profile_page.wait_until_page_loaded()
        assert group_profile_page.is_page_valid()
        assert group_profile_page.get_field_of_science() == new_field_of_science
        assert group_profile_page.get_email() == new_email
        assert group_profile_page.get_phone_number() == new_phone_number


    def test_delete_group(self):
        # add group for delete
        group_name = 'test-delete-group'
        print('adding group {} for delete group test'.format(group_name))
        self.add_group(group_name=group_name)
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
            alert.accept()
            # alert.dismiss()
            print('Alert pop up accepted')
        except:
            print('Error occur at confirming group delete')
        
        # confirm group deleted
        group_link = my_groups_page.get_group_link(group_name)
        assert not group_link

    
    def add_secret(self, cluster_name='my-cluster', secret_name='valid-secret-name', key_name='valid-key-name', key_contents='valid-key-contents'):
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
        self.add_secret(cluster_name=cluster_name, secret_name=secret_name, key_name=key_name, key_contents=key_contents)

        created_secret = '{}: {}'.format(cluster_name, secret_name)
        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()

        created_secret_link = group_profile_page.get_secret_link(created_secret)
        assert created_secret == created_secret_link.text
        created_secret_link.click()

    
    def test_add_secret_wrong_input(self):
        print('test adding new secret with wrong inputs')
        # test cluster not selected
        cluster_not_selected = ''
        self.add_secret(cluster_name=cluster_not_selected)
        secrets_create_page = page.SecretsCreatePage(self.driver)
        cluster_field = secrets_create_page.get_cluster_field()
        message = cluster_field.get_attribute('validationMessage')
        assert message == 'Please select an item in the list.'
        
        # test space in invalid secret name removed
        invalid_secret_name = 'secret name with spaces'
        secret_name_after_send = invalid_secret_name.replace(' ', '')
        secrets_create_page.fill_secret_name(invalid_secret_name)
        secert_name_field = secrets_create_page.get_secret_name_field()
        filled_secret_name = secert_name_field.get_attribute('value')
        assert filled_secret_name == secret_name_after_send

        # test space in invalid key name removed
        invalid_key_name = 'key name with spaces'
        key_name_after_send = invalid_key_name.replace(' ', '')
        secrets_create_page.fill_key_name(invalid_key_name)
        key_name_field = secrets_create_page.get_key_name_field()
        filled_key_name = key_name_field.get_attribute('value')
        assert filled_key_name == key_name_after_send


    def add_mul_secrets(self, num_of_secrets):
        cluster_name = 'my-cluster'
        secret_prefix = 'test-secret'
        key_name_prefix = 'test-key-name'
        key_contents_prefix = 'test-key-contents'
        for i in range(num_of_secrets):
            secret_name = secret_prefix + '-' + str(i)
            key_name = key_name_prefix + '-' + str(i)
            key_contents = key_contents_prefix + '-' + str(i)
            print(secret_name, key_name, key_contents)
            self.add_secret(cluster_name=cluster_name, secret_name=secret_name, key_name=key_name, key_contents=key_contents)
    
    def test_delete_secret(self):
        # first create secret for delete
        group_name = 'my-group'
        cluster_name = 'my-cluster'
        secret_name = 'test-delete-secret'
        key_name = 'test-delete-key-name'
        key_contents = 'test-delete-key-contents'

        print('adding secret {} for delete secret test'.format(secret_name))
        self.add_secret(cluster_name=cluster_name, secret_name=secret_name, key_name=key_name, key_contents=key_contents)

        created_secret = '{}: {}'.format(cluster_name, secret_name)
        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()

        created_secret_link = group_profile_page.get_secret_link(created_secret)
        assert created_secret == created_secret_link.text
        created_secret_link.click() # expand the secret_content_field
        # find the delete button and click()
        secret_field = '{}-{}'.format(cluster_name, secret_name) # 'my-cluster-test-delete-secret'
        group_profile_page.get_secret_link_delete_btn(group_name, secret_field).click()

        try:
            print('before moving to alert')
            alert = group_profile_page.switch_to_alert_popup()
            alert.accept()
            print('Alert pop up accepted')
        except:
            print('Error occur at confirming secret delete')

        # confirm deletion
        created_secret_link = group_profile_page.get_secret_link(created_secret)
        assert not created_secret_link
    

    def tearDown(self):
        # self.driver.implicitly_wait(3)
        time.sleep(7)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()