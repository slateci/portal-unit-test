import sys
import unittest

from selenium.webdriver import Chrome #, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from logtools import CustomLogging

import page

# import os


class PortalBrowsing(unittest.TestCase):
    __logger = CustomLogging('banana').get_logger()

    URL = 'http://localhost:5000/slate_portal'

    def setUp(self):
        options = ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        self.driver = Chrome(options=options)

        self.driver.get(self.URL)


        # test with Firefox, without headless()
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver')
        # test with Firefox, with headless()
        # options = FirefoxOptions()
        # options.headless = True
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver', options=options)

    def test_iterate_clusters_pages(self):
        helpers = Helpers()
        clusters_page = helpers.segue_to_page(self.driver, "clusters")
        page_number = 1
        click_next = True

        while click_next:
            clusters_page.wait_until_clusters_table_loaded()
            clusters_links = clusters_page.get_clusters_links_on_cur_page()
            num_of_links = len(clusters_links)

            # print('page number', page_number)

            for i in range(num_of_links):
                self.__logger.info('Testing cluster page: {}'.format(clusters_links[i].text))
                clusters_links[i].click()
                clusters_profile_page = page.ClusterPublicProfilePage(self.driver, self.__logger)
                self.assertTrue(clusters_profile_page.is_page_valid())
                self.driver.back()
                clusters_page.wait_until_clusters_table_loaded()
                clusters_page.click_cur_page(page_number)
                clusters_page.wait_until_clusters_table_loaded()
                clusters_links = clusters_page.get_clusters_links_on_cur_page()

            next_button = clusters_page.get_next_button()
            if next_button.get_attribute("class").split()[-1] == "disabled":
                click_next = False
            else:
                next_button.click()
                page_number += 1

    def test_iterate_apps_pages(self):
        helpers = Helpers()
        apps_page = helpers.segue_to_page(self.driver, "applications")

        for tab_name in ["Stable Applications", "Incubator Applications"]:
            page_number = 1
            click_next = True
            if tab_name == "Incubator Applications":
                apps_page.click_incubator_apps_tab()
                self.driver.implicitly_wait(
                    3
                )  # implicitly waiting for Incubator Applications tab loaded

            while click_next:
                apps_page.wait_until_apps_table_loaded(tab_name)
                app_links = apps_page.get_app_links_on_cur_page(tab_name)
                number_of_links = len(app_links)

                # print('page number', page_number)

                for i in range(number_of_links):
                    self.__logger.info('Testing app page: {}'.format(app_links[i].text))
                    app_links[i].click()
                    app_detail_page = page.AppsDetailPage(self.driver, self.__logger)
                    self.assertTrue(app_detail_page.is_page_valid())
                    self.driver.back()

                    if tab_name == "Incubator Applications":
                        apps_page.click_incubator_apps_tab()

                    apps_page.wait_until_apps_table_loaded(tab_name)

                    # make sure on the right apps page
                    apps_page.click_cur_page(tab_name, page_number)

                    apps_page.wait_until_apps_table_loaded(tab_name)
                    app_links = apps_page.get_app_links_on_cur_page(tab_name)

                next_button = apps_page.get_next_button(tab_name)
                if next_button.get_attribute("class").split()[-1] == "disabled":
                    click_next = False
                else:
                    next_button.click()
                    page_number += 1

    def test_iterate_instances_pages(self):
        helpers = Helpers()
        # add an new instance
        app_name = "nginx"
        app_suffix = "add-for-test-iterate"
        helpers.add_instance(self.driver, app_name, app_suffix=app_suffix)
        # start clicking pages
        instances_page = helpers.segue_to_page(self.driver, "instances")
        page_number = 1
        click_next = True

        while click_next:
            instances_page.wait_until_instances_table_loaded()
            instance_links = instances_page.get_instance_links_on_cur_page()
            num_of_links = len(instance_links)

            # print('page number', page_number)

            for i in range(num_of_links):
                self.__logger.info('Testing instance page: {}'.format(instance_links[i].text))
                instance_links[i].click()
                instance_detail_page = page.InstanceProfilePage(self.driver, self.__logger)
                self.assertTrue(instance_detail_page.is_page_valid())
                self.driver.back()
                instances_page.wait_until_instances_table_loaded()
                instances_page.click_cur_page(page_number)
                instances_page.wait_until_instances_table_loaded()
                instance_links = instances_page.get_instance_links_on_cur_page()

            next_button = instances_page.get_next_button()
            if next_button.get_attribute("class").split()[-1] == "disabled":
                click_next = False
            else:
                next_button.click()
                page_number += 1

        # delete the new instance
        helpers.delete_instance(self.driver, app_name, app_suffix)

    def test_iterate_secrets_pages(self):
        helpers = Helpers()

        # create a group of secrets
        added_secrets = helpers.add_mul_secrets(self.driver)
        # iterate secrets
        secrets_page = helpers.segue_to_page(self.driver, "secrets")
        page_number = 1
        click_next = True

        while click_next:
            secrets_page.wait_until_secrets_table_loaded()
            secrets_links = secrets_page.get_secret_links_on_cur_page()
            num_of_links = len(secrets_links)
            # print(num_of_links)
            # print('page number', page_number)

            for i in range(num_of_links):
                self.__logger.info('Testing secret page: {}'.format(secrets_links[i].text))
                secrets_links[i].click()
                group_profile_page = page.GroupProfilePage(self.driver, self.__logger)
                self.assertTrue(group_profile_page.is_page_valid())
                self.driver.back()

                secrets_page.wait_until_secrets_table_loaded()
                secrets_page.click_cur_page(page_number)
                secrets_page.wait_until_secrets_table_loaded()
                secrets_links = secrets_page.get_secret_links_on_cur_page()

            next_button = secrets_page.get_next_button()
            if next_button.get_attribute("class").split()[-1] == "disabled":
                click_next = False
            else:
                next_button.click()
                page_number += 1

        # delete the added secrets
        for secret in added_secrets["secret_names"]:
            helpers.delete_secret(
                self.driver,
                added_secrets["group_name"],
                added_secrets["cluster_name"],
                secret,
            )

    def test_iterate_my_groups_pages(self):
        helpers = Helpers()
        my_groups_page = helpers.segue_to_page(self.driver, "my_groups")
        page_number = 1
        click_next = True

        while click_next:
            my_groups_page.wait_until_groups_table_loaded()
            my_groups_links = my_groups_page.get_group_links_on_cur_page()
            num_of_links = len(my_groups_links)

            # print('page number', page_number)

            for i in range(num_of_links):
                self.__logger.info('Testing group page: {}'.format(my_groups_links[i].text))
                my_groups_links[i].click()
                my_groups_detail_page = page.GroupProfilePage(self.driver, self.__logger)
                self.assertTrue(my_groups_detail_page.is_page_valid())
                self.driver.back()
                my_groups_page.wait_until_groups_table_loaded()
                my_groups_page.click_cur_page(page_number)
                my_groups_page.wait_until_groups_table_loaded()
                my_groups_links = my_groups_page.get_group_links_on_cur_page()

            next_button = my_groups_page.get_next_button()
            if next_button.get_attribute("class").split()[-1] == "disabled":
                click_next = False
            else:
                next_button.click()
                page_number += 1

    def test_iterate_all_groups_pages(self):
        helpers = Helpers()
        all_groups_page = helpers.segue_to_page(self.driver, "all_groups")
        page_number = 1
        click_next = True

        while click_next:
            all_groups_page.wait_until_groups_table_loaded()
            all_groups_links = all_groups_page.get_group_links_on_cur_page()
            num_of_links = len(all_groups_links)

            # print('page number', page_number)

            for i in range(num_of_links):
                self.__logger.info('Testing group page: {}'.format(all_groups_links[i].text))
                all_groups_links[i].click()
                all_groups_detail_page = page.GroupProfilePage(self.driver, self.__logger)
                self.assertTrue(all_groups_detail_page.is_page_valid())
                self.driver.back()
                all_groups_page.wait_until_groups_table_loaded()
                all_groups_page.click_cur_page(page_number)
                all_groups_page.wait_until_groups_table_loaded()
                all_groups_links = all_groups_page.get_group_links_on_cur_page()

            next_button = all_groups_page.get_next_button()
            if next_button.get_attribute("class").split()[-1] == "disabled":
                click_next = False
            else:
                next_button.click()
                page_number += 1

    def test_check_cli_access_page(self):
        helpers = Helpers()
        helpers.segue_to_page(self.driver, "cli_access")

    def tearDown(self):
        # self.driver.implicitly_wait(3)
        # time.sleep(3)
        self.driver.close()


class FuncTests(unittest.TestCase):
    __logger = CustomLogging('banana').get_logger()

    URL = 'http://localhost:5000/slate_portal'

    def setUp(self):
        options = ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        self.driver = Chrome(options=options)

        self.driver.get(self.URL)

        # test with Firefox, without headless()
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver')
        # test with Firefox, with headless()
        # options = FirefoxOptions()
        # options.headless = True
        # options.headless = False
        # self.driver = Firefox(executable_path='/opt/WebDriver/bin/geckodriver', options=options)

    def test_add_and_delete_instance(self):
        helpers = Helpers()
        self.__logger.info('1) test_add_and_delete_instance')
        # add a new instance
        app_name = "nginx"
        app_suffix = "test-add-and-delete"
        helpers.add_instance(self.driver, app_name, app_suffix=app_suffix)

        # delete the instance
        helpers.delete_instance(self.driver, app_name, app_suffix)

    def test_add_instance_wrong_input(self):
        helpers = Helpers()
        self.__logger.info('2) test_add_instance_with_wrong_input')
        app_name = "nginx"
        app_suffix = "test-add-with-wrong-input"
        apps_page = helpers.segue_to_page(self.driver, "applications")

        apps_page.wait_until_apps_table_loaded("Stable Applications")
        app_link = apps_page.get_app_link(app_name)

        if app_link:
            self.__logger.info('installing {}'.format(app_link.text))
            app_link.click()
            app_detail_page = page.AppsDetailPage(self.driver, self.__logger)
            self.assertTrue(app_detail_page.is_page_valid())
            app_detail_page.wait_until_ready_for_install()
            app_detail_page.click_intall_app()

            # test missing group name
            app_create_page = page.AppCreatePage(self.driver, self.__logger)
            self.assertTrue(app_create_page.is_page_valid())
            app_create_page.fill_group(group_name="")
            app_create_page.click_next()

            group_field = app_create_page.get_group_field()
            message = group_field.get_attribute("validationMessage")
            self.assertEqual(message, "Please select an item in the list.")

            # select a valid group and proceed to next page
            app_create_page.fill_group()
            app_create_page.click_next()

            # test missing cluster name
            app_create_final_page = page.AppCreateFinalPage(self.driver, self.__logger)
            self.assertTrue(app_create_final_page.is_page_valid())
            app_create_final_page.fill_cluster(cluster_name="")
            app_create_final_page.fill_configuration(app_suffix)
            app_create_final_page.click_install()

            cluster_field = app_create_final_page.get_cluster_field()
            message = cluster_field.get_attribute("validationMessage")
            self.assertEqual(message, "Please select an item in the list.")

    def test_add_and_delete_group(self):
        self.__logger.info('3) test_add_and_delete_group')
        helpers = Helpers()
        # add group
        group_name = "test-add-and-delete-group"
        self.__logger.info('adding group {} for delete group test'.format(group_name))
        helpers.add_group(self.driver, group_name=group_name)
        # delete group
        self.__logger.info('test_delete_group')
        helpers.delete_group(self.driver, group_name)

    def test_add_group_with_wrong_inputs(self):
        self.__logger.info('4) test_add_group_with_wrong_inputs')
        helpers = Helpers()
        # test invalid group name
        invalid_group_name = "valid@name"
        helpers.attempt_add_group(self.driver, group_name=invalid_group_name)
        create_new_group_page = page.CreateNewGroupPage(self.driver, self.__logger)
        group_name_field = create_new_group_page.get_group_name_field()
        message = group_name_field.get_attribute("validationMessage")
        self.assertEqual(message, "Please match the requested format.")

        # test empty phone number field
        empty_phone_number = ""
        helpers.attempt_add_group(self.driver, phone_number=empty_phone_number)
        create_new_group_page = page.CreateNewGroupPage(self.driver, self.__logger)
        phone_number_field = create_new_group_page.get_phone_number_field()
        message = phone_number_field.get_attribute("validationMessage")
        self.assertEqual(message, "Please fill out this field.")

        # test invalid email (without '@')
        invalid_email = "slate-slateci.io"
        helpers.attempt_add_group(self.driver, email=invalid_email)
        create_new_group_page = page.CreateNewGroupPage(self.driver, self.__logger)
        email_field = create_new_group_page.get_email_field()
        message = email_field.get_attribute("validationMessage")
        self.assertEqual(
            message,
            "Please include an '@' in the email address. '{}' is missing an '@'.".format(
                invalid_email
            ),
        )

        # test empty field of science
        empty_field_of_science = ""
        helpers.attempt_add_group(self.driver, field_of_science=empty_field_of_science)
        create_new_group_page = page.CreateNewGroupPage(self.driver, self.__logger)
        science_field = create_new_group_page.get_field_of_science()
        message = science_field.get_attribute("validationMessage")
        self.assertEqual(message, "Please select an item in the list.")

    def test_edit_group(self):
        self.__logger.info('5) test_edit_group')
        helpers = Helpers()
        # add group for edit
        group_name = "test-edit-group"
        self.__logger.info('adding group {} for edit group test'.format(group_name))
        helpers.add_group(self.driver, group_name=group_name)
        # edit group
        self.__logger.info('test_edit_group')
        my_groups_page = helpers.segue_to_page(self.driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(self.driver, self.__logger)
        self.assertTrue(group_profile_page.is_page_valid())
        group_profile_page.wait_until_page_loaded()
        group_profile_page.get_edit_btn().click()

        group_edit_page = page.GroupEditPage(self.driver, self.__logger)
        self.assertTrue(group_edit_page.is_page_valid())
        group_edit_page.wait_until_form_loaded()

        new_email = "selenium-test@slateci.io"
        new_phone_number = "777-7777"
        new_field_of_science = "Physics"
        new_description = "Testing group edit functionality"
        helpers.edit_group_on_edit_page(
            group_edit_page,
            email=new_email,
            phone_number=new_phone_number,
            field_of_science=new_field_of_science,
            description=new_description,
        )

        # confirm group info updated
        group_profile_page.wait_until_page_loaded()
        self.assertTrue(group_profile_page.is_page_valid())
        self.assertEqual(
            group_profile_page.get_field_of_science(), new_field_of_science
        )
        self.assertEqual(group_profile_page.get_email(), new_email)
        self.assertEqual(group_profile_page.get_phone_number(), new_phone_number)

        # delete the group
        helpers.delete_group(self.driver, group_name)

    def test_edit_group_with_wrong_inputs(self):
        self.__logger.info('6) test_edit_new_group_with_wrong_inputs')
        helpers = Helpers()
        # add group for edit with wrong input
        group_name = "test-edit-group-wrong-input"
        self.__logger.info('adding group {} for edit group test'.format(group_name))
        helpers.add_group(self.driver, group_name=group_name)
        # edit with wrong input
        self.__logger.info('test_edit_group_with_wrong_input')
        my_groups_page = helpers.segue_to_page(self.driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(self.driver, self.__logger)
        self.assertTrue(group_profile_page.is_page_valid())
        group_profile_page.wait_until_page_loaded()
        group_profile_page.get_edit_btn().click()

        group_edit_page = page.GroupEditPage(self.driver, self.__logger)
        self.assertTrue(group_edit_page.is_page_valid())
        group_edit_page.wait_until_form_loaded()

        # test invalid email input
        invalid_email = "selenium-testslateci.io"
        helpers.edit_group_on_edit_page(group_edit_page, email=invalid_email)
        email_field = group_edit_page.get_email_field()
        message = email_field.get_attribute("validationMessage")
        self.assertEqual(
            message,
            "Please include an '@' in the email address. '{}' is missing an '@'.".format(
                invalid_email
            ),
        )

        # test missing phone number
        missing_phone_number = ""
        helpers.edit_group_on_edit_page(
            group_edit_page, phone_number=missing_phone_number
        )
        phone_number_field = group_edit_page.get_phone_number_field()
        message = phone_number_field.get_attribute("validationMessage")
        self.assertEqual(message, "Please fill out this field.")

        # # test empty field of science
        # empty_field_of_science = ''
        # self.edit_group_on_edit_page(group_edit_page, field_of_science=empty_field_of_science)
        # science_field = group_edit_page.get_science_field()
        # message = science_field.get_attribute('validationMessage')
        # print(message)

        # delete the group
        helpers.delete_group(self.driver, group_name)

    def in_progress_test_edit_cluster_in_group(self):
        helpers = Helpers()
        group_name = "my-group"
        cluster_name = "my-cluster"
        my_groups_page = helpers.segue_to_page(self.driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()
        # enter the group page
        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()
        group_profile_page = page.GroupProfilePage(self.driver, self.__logger)
        self.assertTrue(group_profile_page.is_page_valid())
        group_profile_page.wait_until_page_loaded()
        # enter the cluster page
        cluster_link = group_profile_page.get_cluster_link(cluster_name)
        cluster_link.click()

        cluster_profile_page = page.ClusterProfilePage(self.driver, self.__logger)
        self.assertTrue(cluster_profile_page.is_page_valid())
        cluster_profile_page.wait_until_page_loaded()

        # test edit button
        edit_info_btn = cluster_profile_page.get_edit_info_btn()
        edit_info_btn.click()

        cluster_edit_page = page.ClusterEditPage(self.driver, self.__logger)
        self.assertTrue(cluster_edit_page.is_page_valid())
        cluster_edit_page.wait_until_page_loaded()

        cluster_edit_page.set_org_field("SLATE1")
        # cluster_edit_page.set_latitude_field('0.05')
        # cluster_edit_page.set_longitude_field('0.06')
        cluster_edit_page.get_latitude_field().clear()
        cluster_edit_page.get_longitude_field().clear()

        cluster_edit_page.get_update_btn().click()

        nextPage = page.BasePage(self.driver, self.__logger)
        self.assertTrue(nextPage.is_page_valid())

        # test group selector
        # cluster_profile_page.set_group_selector('test-add-group')
        # add_group_btn = cluster_profile_page.get_add_group_btn(cluster_name)
        # add_group_btn.click()

    def test_add_group_to_cluster(self):
        self.__logger.info('7) test_add_group_to_cluster')
        helpers = Helpers()
        # add group
        added_group_name = "test-add-group-to-cluster"
        self.__logger.info('adding group {} for delete group test'.format(added_group_name))
        helpers.add_group(self.driver, group_name=added_group_name)

        # add group to cluster
        group_name = "my-group"
        cluster_name = "my-cluster"
        my_groups_page = helpers.segue_to_page(self.driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()
        # enter the group page
        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()
        group_profile_page = page.GroupProfilePage(self.driver, self.__logger)
        self.assertTrue(group_profile_page.is_page_valid())
        group_profile_page.wait_until_page_loaded()
        # enter the cluster page
        cluster_link = group_profile_page.get_cluster_link(cluster_name)
        cluster_link.click()

        cluster_profile_page = page.ClusterProfilePage(self.driver, self.__logger)
        self.assertTrue(cluster_profile_page.is_page_valid())
        cluster_profile_page.wait_until_page_loaded()

        # test group selector
        cluster_profile_page.set_group_selector(added_group_name)
        add_group_btn = cluster_profile_page.get_add_group_btn(cluster_name)
        add_group_btn.click()

        # confirm group added to cluster
        check_added_group = cluster_profile_page.get_added_group_link(
            group_name, cluster_name, added_group_name
        )
        self.assertEqual(added_group_name, check_added_group.text)
        # delete group
        helpers.delete_group(self.driver, added_group_name)

    def test_revoke_group_from_cluster(self):
        self.__logger.info('8) test_revoke_group_from_cluster')
        helpers = Helpers()
        # add group
        added_group_name = "test-add-group-to-revoke-from-cluster"
        self.__logger.info('adding group {} for delete group test'.format(added_group_name))
        helpers.add_group(self.driver, group_name=added_group_name)

        # add group to cluster
        group_name = "my-group"
        cluster_name = "my-cluster"
        my_groups_page = helpers.segue_to_page(self.driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()
        # enter the group page
        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()
        group_profile_page = page.GroupProfilePage(self.driver, self.__logger)
        self.assertTrue(group_profile_page.is_page_valid())
        group_profile_page.wait_until_page_loaded()
        # enter the cluster page
        cluster_link = group_profile_page.get_cluster_link(cluster_name)
        cluster_link.click()

        cluster_profile_page = page.ClusterProfilePage(self.driver, self.__logger)
        self.assertTrue(cluster_profile_page.is_page_valid())
        cluster_profile_page.wait_until_page_loaded()

        # test group selector
        cluster_profile_page.set_group_selector(added_group_name)
        add_group_btn = cluster_profile_page.get_add_group_btn(cluster_name)
        add_group_btn.click()

        # confirm group added to cluster
        check_added_group = cluster_profile_page.get_added_group_link(
            group_name, cluster_name, added_group_name
        )
        self.assertEqual(added_group_name, check_added_group.text)

        # revoke group
        revoke_group_btn = cluster_profile_page.get_revoke_btn(added_group_name)
        revoke_group_btn.click()

        # confirm group revoke
        check_added_group = cluster_profile_page.get_added_group_link(
            group_name, cluster_name, added_group_name
        )
        self.assertFalse(check_added_group)

        # delete group
        helpers.delete_group(self.driver, added_group_name)

    def test_add_and_delete_secret(self):
        self.__logger.info('9) test_add_and_delete_secret')
        group_name = "my-group"
        cluster_name = "my-cluster"
        secret_name = "test-secret-with-helper"
        key_name = "test-key-name"
        key_contents = "test-key-contents"
        helpers = Helpers()
        # add the secret
        helpers.add_secret(
            self.driver,
            cluster_name=cluster_name,
            secret_name=secret_name,
            key_name=key_name,
            key_contents=key_contents,
        )
        # confirm secret added
        created_secret = "{}: {}".format(cluster_name, secret_name)
        group_profile_page = page.GroupProfilePage(self.driver, self.__logger)
        self.assertTrue(group_profile_page.is_page_valid())

        created_secret_link = group_profile_page.get_secret_link(created_secret)
        self.assertEqual(created_secret, created_secret_link.text)
        created_secret_link.click()

        # delete the secret
        helpers.delete_secret(self.driver, group_name, cluster_name, secret_name)

    def test_add_secret_wrong_inputs(self):
        self.__logger.info('10) test_add_ecret_with_wrong_inputs')
        # test cluster not selected
        cluster_not_selected = ""
        helpers = Helpers()
        helpers.add_secret(self.driver, cluster_name=cluster_not_selected)
        secrets_create_page = page.SecretsCreatePage(self.driver, self.__logger)
        cluster_field = secrets_create_page.get_cluster_field()
        message = cluster_field.get_attribute("validationMessage")
        self.assertEqual(message, "Please select an item in the list.")

        # test space in invalid secret name removed
        invalid_secret_name = "secret name with spaces"
        secret_name_after_send = invalid_secret_name.replace(" ", "")
        secrets_create_page.fill_secret_name(invalid_secret_name)
        secert_name_field = secrets_create_page.get_secret_name_field()
        filled_secret_name = secert_name_field.get_attribute("value")
        self.assertEqual(filled_secret_name, secret_name_after_send)

        # test space in invalid key name removed
        invalid_key_name = "key name with spaces"
        key_name_after_send = invalid_key_name.replace(" ", "")
        secrets_create_page.fill_key_name(invalid_key_name)
        key_name_field = secrets_create_page.get_key_name_field()
        filled_key_name = key_name_field.get_attribute("value")
        self.assertEqual(filled_key_name, key_name_after_send)

    def tearDown(self):
        # time.sleep(5)
        self.driver.close()


class Helpers:
    __logger = CustomLogging('banana').get_logger()
    __testcase = unittest.TestCase()

    def segue_to_page(self, driver, page_name):
        start_page = page.BasePage(driver, self.__logger)
        self.__testcase.assertTrue(start_page.is_page_valid())
        cur_page = None
        if page_name == "clusters":
            start_page.go_to_clusters_page()
            cur_page = page.ClustersPage(driver, self.__logger)
        elif page_name == "applications":
            start_page.go_to_apps_page()
            cur_page = page.AppsPage(driver, self.__logger)
        elif page_name == "secrets":
            start_page.go_to_secrets_page()
            cur_page = page.SecretsPage(driver, self.__logger)
        elif page_name == "instances":
            start_page.go_to_instances_page()
            cur_page = page.InstancesPage(driver, self.__logger)
        elif page_name == "my_groups":
            start_page.go_to_my_groups_page()
            cur_page = page.MyGroupsPage(driver, self.__logger)
        elif page_name == "all_groups":
            start_page.go_to_all_groups_page()
            cur_page = page.GroupsPage(driver, self.__logger)
        elif page_name == "cli_access":
            start_page.go_to_cli_access_page()
            cur_page = page.CLIAccessPage(driver, self.__logger)
        self.__testcase.assertTrue(cur_page.is_page_valid())
        return cur_page

    def add_instance(self, driver, app_name, app_suffix=""):
        apps_page = self.segue_to_page(driver, "applications")
        installed = False
        # find the app

        instance_detail_page = None

        apps_page.wait_until_apps_table_loaded("Stable Applications")
        app_link = apps_page.get_app_link(app_name)

        if app_link:
            # print('installing', app_link.text)
            app_link.click()
            app_detail_page = page.AppsDetailPage(driver, self.__logger)
            self.__testcase.assertTrue(app_detail_page.is_page_valid())
            app_detail_page.wait_until_ready_for_install()
            app_detail_page.click_intall_app()

            app_create_page = page.AppCreatePage(driver, self.__logger)
            self.__testcase.assertTrue(app_create_page.is_page_valid())
            app_create_page.fill_group()
            app_create_page.click_next()

            app_create_final_page = page.AppCreateFinalPage(driver, self.__logger)
            self.__testcase.assertTrue(app_create_final_page.is_page_valid())
            app_create_final_page.fill_cluster()
            app_create_final_page.fill_configuration(app_suffix)
            app_create_final_page.click_install()

            # enter instance detail page; check instance name
            instance_detail_page = page.InstanceProfilePage(driver, self.__logger)
            self.__testcase.assertTrue(instance_detail_page.is_page_valid())
            instance_detail_page.wait_until_page_loaded()

            installed_app_name = instance_detail_page.get_app_name()
            self.__testcase.assertEqual(installed_app_name, app_name)

            # change install flag to true
            installed = True

        self.__testcase.assertTrue(installed)
        self.__logger.info('Instance: {} installed'.format(app_name))
        return instance_detail_page

    def delete_instance(self, driver, app_name, app_suffix):
        instances_page = self.segue_to_page(driver, "instances")
        instances_page.wait_until_instances_table_loaded()
        instance_name = app_name + "-" + app_suffix

        instance_link = instances_page.get_instance_link(instance_name)

        instance_link.click()
        instance_detail_page = page.InstanceProfilePage(driver)
        self.__testcase.assertTrue(instance_detail_page.is_page_valid())

        instance_name = instance_detail_page.get_instance_name()
        cluster_name = instance_detail_page.get_cluster_name()
        group_name = instance_detail_page.get_group_name()

        self.__logger.info('Click Delete button of {}'.format(instance_name))
        instance_detail_page.get_delete_button().click()
        try:
            alert = instance_detail_page.switch_to_alert_popup()
            # time.sleep(1)
            alert.accept()
            self.__logger.info('Alert pop up accepted')
        except:
            self.__logger.debug('Error occur at confirming instance delete')
            pass

        # check instance deleted
        instances_page.wait_until_instances_table_loaded()
        instance_link = instances_page.get_instance_link(instance_name)
        self.__testcase.assertFalse(instance_link)
        self.__logger.info('Instance {} successfully deleted'.format(instance_name))

    def add_group(
        self,
        driver,
        group_name="valid-name",
        phone_number="555-5555",
        email="slate@slateci.io",
        field_of_science="Biology",
    ):
        my_groups_page = self.segue_to_page(driver, "my_groups")
        my_groups_page.get_register_new_group_btn().click()
        create_new_group = page.CreateNewGroupPage(driver, self.__logger)
        # create_new_group.wait_until_form_loaded()

        create_new_group.fill_group_name(group_name)
        create_new_group.fill_phone_number(phone_number)
        create_new_group.fill_email(email)
        create_new_group.fill_field_of_science(field_of_science)
        create_new_group.create_group()

        group_profile_page = page.GroupProfilePage(driver, self.__logger)
        group_profile_page.wait_until_page_loaded()
        self.__testcase.assertTrue(group_profile_page.is_page_valid())
        # confirm group added
        self.__testcase.assertEqual(group_name, group_profile_page.get_group_name())
        self.__logger.info('group {} successfully added'.format(group_name))

    def attempt_add_group(
        self,
        driver,
        group_name="valid-name",
        phone_number="555-5555",
        email="slate@slateci.io",
        field_of_science="Biology",
    ):
        """
        this function is a helper function used in test_add_group_with_wrong_input()
        it attempts to add group without confirming the group is added
        """
        my_groups_page = self.segue_to_page(driver, "my_groups")
        my_groups_page.get_register_new_group_btn().click()
        create_new_group = page.CreateNewGroupPage(driver, self.__logger)
        # create_new_group.wait_until_form_loaded()

        create_new_group.fill_group_name(group_name)
        create_new_group.fill_phone_number(phone_number)
        create_new_group.fill_email(email)
        create_new_group.fill_field_of_science(field_of_science)
        create_new_group.create_group()

        # group_profile_page = page.BasePage(driver)
        # self.__testcase.assertTrue(group_profile_page.is_page_valid())

    def delete_group(self, driver, group_name):
        my_groups_page = self.segue_to_page(driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(driver, self.__logger)
        self.__testcase.assertTrue(group_profile_page.is_page_valid())
        group_profile_page.wait_until_page_loaded()
        group_profile_page.get_delete_group_btn().click()
        try:
            alert = group_profile_page.switch_to_alert_popup()
            # time.sleep(1)
            alert.accept()
            # alert.dismiss()
            self.__logger.info('Alert pop up accepted')
        except:
            self.__logger.debug('Error occur at confirming group delete')
            pass

        # confirm group deleted
        group_link = my_groups_page.get_group_link(group_name)
        self.__testcase.assertFalse(group_link)
        self.__logger.info('group {} successfully deleted'.format(group_name))

    def add_secret(
        self,
        driver,
        group_name="my-group",
        cluster_name="my-cluster",
        secret_name="valid-secret-name",
        key_name="valid-key-name",
        key_contents="valid-key-contents",
    ):
        # group_name = 'my-group'
        my_groups_page = self.segue_to_page(driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()

        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()

        group_profile_page = page.GroupProfilePage(driver, self.__logger)
        self.__testcase.assertTrue(group_profile_page.is_page_valid())
        group_profile_page.wait_until_page_loaded

        group_profile_page.get_secrets_tab().click()
        group_profile_page.get_new_secret_btn().submit()

        secrets_create_page = page.SecretsCreatePage(driver, self.__logger)
        secrets_create_page.fill_form_and_submit(
            cluster_name, secret_name, key_name, key_contents
        )

    def add_mul_secrets(self, driver, num_of_secrets=5):
        group_name = "my-group"
        cluster_name = "my-cluster"
        secret_prefix = "test-secret"
        key_name_prefix = "test-key-name"
        key_contents_prefix = "test-key-contents"

        added_secrets = {
            "group_name": group_name,
            "cluster_name": cluster_name,
            "secret_names": [],
        }

        for i in range(num_of_secrets):
            secret_name = secret_prefix + "-" + str(i)
            key_name = key_name_prefix + "-" + str(i)
            key_contents = key_contents_prefix + "-" + str(i)
            added_secrets["secret_names"].append(secret_name)
            # print(secret_name, key_name, key_contents)
            self.add_secret(
                driver,
                group_name=group_name,
                cluster_name=cluster_name,
                secret_name=secret_name,
                key_name=key_name,
                key_contents=key_contents,
            )

        return added_secrets

    def delete_secret(self, driver, group_name, cluster_name, secret_name):
        # enter group profile page
        my_groups_page = self.segue_to_page(driver, "my_groups")
        my_groups_page.wait_until_groups_table_loaded()
        group_link = my_groups_page.get_group_link(group_name)
        group_link.click()
        # prepare to delete secret
        created_secret = "{}: {}".format(cluster_name, secret_name)
        group_profile_page = page.GroupProfilePage(driver, self.__logger)
        self.__testcase.assertTrue(group_profile_page.is_page_valid())
        # group_profile_page.wait_until_page_loaded
        # click secrets tab
        group_profile_page.get_secrets_tab().click()

        created_secret_link = group_profile_page.get_secret_link(created_secret)
        self.__testcase.assertEqual(created_secret, created_secret_link.text)
        created_secret_link.click()  # expand the secret_content_field
        # find the delete button and click()
        secret_field = "{}-{}".format(
            cluster_name, secret_name
        )  # 'my-cluster-test-delete-secret'
        group_profile_page.get_secret_link_delete_btn(group_name, secret_field).click()

        try:
            self.__logger.info('attempt to delete secret: {}'.format(secret_name))
            alert = group_profile_page.switch_to_alert_popup()
            alert.accept()
            self.__logger.info('secret {} is deleted'.format(secret_name))
        except:
            self.__logger.debug('Error occur at confirming secret delete')
            pass

        # confirm deletion
        created_secret_link = group_profile_page.get_secret_link(created_secret)
        self.__testcase.assertFalse(created_secret_link)

    def edit_group_on_edit_page(
        self,
        group_edit_page,
        email="selenium-test@slateci.io",
        phone_number="777-7777",
        field_of_science="Physics",
        description="Testing group edit functionality",
    ):
        group_edit_page.update_email(email)
        group_edit_page.update_phone_number(phone_number)
        group_edit_page.update_field_of_science(field_of_science)
        group_edit_page.update_description(description)
        # click update
        group_edit_page.update_group()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PortalBrowsing.URL = sys.argv.pop()
        FuncTests.URL = sys.argv.pop()
    unittest.main()
