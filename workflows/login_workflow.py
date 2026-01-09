class LoginWorkflow:
    def __init__(self, driver):
        from pages.login_page import LoginPage
        self.login_page = LoginPage(driver)

    def login(self, email, password):
        self.login_page.open_login_page()
        self.login_page.login(email, password)
