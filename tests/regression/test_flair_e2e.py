def test_flair_end_to_end(driver):
    from data.login_data import LoginData
    from data.source_data import DEFAULT_SUPPLIER, item1
    from workflows.login_workflow import LoginWorkflow
    from workflows.sourcing_workflow import SourcingWorkflow
    from workflows.approval_workflow import ApprovalWorkflow

    login = LoginData()

    LoginWorkflow(driver).login(login.buyer_email, login.buyer_password)
    SourcingWorkflow(driver).create_supplier_with_item(DEFAULT_SUPPLIER, item1)

    LoginWorkflow(driver).login(login.admin_email, login.admin_password)
    ApprovalWorkflow(driver).approve()
