import unittest
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import page
import time
import sys


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
        dashboard_page = page.DashboardPage(self.driver)
        assert dashboard_page.is_page_valid()
        cur_page = None
        if page_name == 'clusters':
            dashboard_page.go_to_clusters_page()
            cur_page = page.ClustersPage(self.driver)
        elif page_name == 'applications':
            dashboard_page.go_to_apps_page()
            cur_page = page.AppsPage(self.driver)
        elif page_name == 'instances':
            dashboard_page.go_to_instances_page()
            cur_page = page.InstancesPage(self.driver)
        elif page_name == 'my_groups':
            dashboard_page.go_to_my_groups_page()
            cur_page = page.MyGroupsPage(self.driver)
        elif page_name == 'all_groups':
            dashboard_page.go_to_all_groups_page()
            cur_page = page.GroupsPage(self.driver)
        elif page_name == 'cli_access':
            dashboard_page.go_to_cli_access_page()
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

    def segue_to_page(self, page_name):
        dashboard_page = page.DashboardPage(self.driver)
        assert dashboard_page.is_page_valid()
        cur_page = None
        if page_name == 'clusters':
            dashboard_page.go_to_clusters_page()
            cur_page = page.ClustersPage(self.driver)
        elif page_name == 'instances':
            dashboard_page.go_to_instances_page()
            cur_page = page.InstancesPage(self.driver)
        elif page_name == 'my_groups':
            dashboard_page.go_to_my_groups_page()
            cur_page = page.MyGroupsPage(self.driver)
        assert cur_page.is_page_valid()
        return cur_page
    
    def test_instance_delete_dismiss(self):
        instances_page = self.segue_to_page('instances')
        instances_page.create_nginx_instance()
        
        instances_page.wait_until_instances_table_loaded()
        instance_links = instances_page.get_instance_links_on_cur_page()
        
        if not instance_links:
            print('there is not instance to be deleted')
        else:
            print('attempting to delete instance:', instance_links[0].text)
            instance_links[0].click()
            instance_detail_page = page.InstanceProfilePage(self.driver)
            assert instance_detail_page.is_page_valid()

            instance_name = instance_detail_page.get_instance_name()
            cluster_name = instance_detail_page.get_cluster_name()
            group_name = instance_detail_page.get_group_name()

            print('print instance name:', instance_name)
            print('print cluster name:', cluster_name)
            print('print group name:', group_name)

            if cluster_name == 'my-cluster' and group_name == 'my-group':
                print('Click Delete button of instance:', instance_name)
                instance_detail_page.get_delete_button().click()
                try:
                    alert = instance_detail_page.switch_to_alert_popup()
                    time.sleep(1)
                    alert.dismiss()
                    print('Alert pop up dismissed')
                except:
                    print('Alert pop up not dismissed')

                try:
                    self.driver.back()
                    self.driver.back()
                except:
                    print('Back button does not work')
    

    def test_instance_delete_accept(self):
        instances_page = self.segue_to_page('instances')
        
        instances_page.wait_until_instances_table_loaded()
        instance_links = instances_page.get_instance_links_on_cur_page()

        if not instance_links:
            print('there is not instance to be deleted')
        else:
            print('attempting to delete instance:', instance_links[0].text)
            instance_links[0].click()
            instance_detail_page = page.InstanceProfilePage(self.driver)
            assert instance_detail_page.is_page_valid()

            instance_name = instance_detail_page.get_instance_name()
            cluster_name = instance_detail_page.get_cluster_name()
            group_name = instance_detail_page.get_group_name()

            print('print instance name:', instance_name)
            print('print cluster name:', cluster_name)
            print('print group name:', group_name)

            if cluster_name == 'my-cluster' and group_name == 'my-group':
                print('Click Delete button of instance:', instance_name)
                instance_detail_page.get_delete_button().click()
                try:
                    alert = instance_detail_page.switch_to_alert_popup()
                    time.sleep(1)
                    alert.accept()
                    print('Alert pop up accepted')
                except:
                    print('Error occur at confirming instance delete')
                
                instances_page.wait_until_instances_table_loaded()
                instance_links = instances_page.get_instance_links_on_cur_page()
                existing_instances = [instance_links[i].text for i in instance_links]
                assert instance_name not in existing_instances
                print('Instance {} successfully deleted'.format(instance_name))


    def test_add_new_group(self):
        my_groups_page = self.segue_to_page('my_groups')
        my_groups_page.get_register_new_group_btn().click()
        create_new_group = page.CreateNewGroupPage(self.driver)
        create_new_group.fill_group_name('my-group')
        create_new_group.fill_field_of_science('Biology')
        create_new_group.create_group()
        
        group_profile_page = page.GroupProfilePage(self.driver)
        assert group_profile_page.is_page_valid()
    
    def tearDown(self):
        # self.driver.implicitly_wait(3)
        time.sleep(3)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()