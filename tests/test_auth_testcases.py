def test_TC_01_User_registration(pages, faker) -> None:
    faker.seed_instance()
    pages.login.register_first_time(faker.name(), faker.last_name(), faker.password(), faker.email())
    pages.login.validate_registration()


def test_TC_02_Login_with_valid_credentials(pages, extra) -> None:
    # Fetch credentials once from Excel
    creds = pages.testdata.get_credentials("TC_02")
    # Step 1: Navigate to login
    pages.login.click_on_log_in_link()
    # Step 2: Enter credentials (username + password from Excel)
    pages.login.enter_valid_login_credentials(creds["username"], creds["password"])
    # Step 3: Validate login
    pages.login.validate_login_existing_user()



def test_TC_03_Login_with_valid_credentials(pages) -> None:
    creds = pages.testdata.get_credentials("TC_03")
    pages.login.click_on_log_in_link()
    pages.login.enter_valid_login_credentials(creds["username"], creds["password"])
    pages.login.validate_incorrect_login()
