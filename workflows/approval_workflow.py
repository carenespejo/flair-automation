class ApprovalWorkflow:
    def __init__(self, driver):
        from pages.sourcing_page import SourcingPage
        self.page = SourcingPage(driver)

    def approve(self):
        self.page.click_approve_button()
        self.page.confirm_approve()

    def reject(self, reason):
        self.page.click_reject_button()
        self.page.fill_rejection_reason(reason)
        self.page.confirm_reject()
