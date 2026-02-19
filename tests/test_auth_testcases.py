def test_TC_01_User_registration(pages) -> None:
    pages.login.register_first_time("abcde", "efgd", "asdfgh", "5navidm@gmail.com")
    pages.login.validate_registration()


def test_TC_02_Login_with_valid_credentials(pages, extra) -> None:
    # Fetch credentials once from Excel
    creds = pages.testdata.get_credentials("TC_02")

    # Step 1: Navigate to login
    pages.login.click_on_log_in_link()
    extra.append(pages.testdata.extras.text("Clicked on login link"))

    # Step 2: Enter credentials (username + password from Excel)
    pages.login.enter_valid_login_credentials(creds["username"], creds["password"])
    extra.append(pages.testdata.extras.text(f"Entered credentials for {creds['username']}"))

    # Step 3: Validate login
    pages.login.validate_login_existing_user()
    extra.append(pages.testdata.extras.text("Validated login for existing user"))



def test_TC_03_Login_with_valid_credentials(pages) -> None:
    pages.login.click_on_log_in_link()
    pages.login.enter_valid_login_credentials("5navidm@gmail.com", "asdfg0")
    pages.login.validate_incorrect_login()
