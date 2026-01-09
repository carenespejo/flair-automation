class SourcingWorkflow:
    def __init__(self, driver):
        from pages.sourcing_page import SourcingPage
        self.page = SourcingPage(driver)

    def create_supplier_with_item(self, supplier, item):
        self.page.open_sourcing_page()
        self.page.click_new_source_button()

        self.page.fill_supplier_name(supplier.supplier_name)
        self.page.fill_supplier_address(supplier.supplier_address)
        self.page.fill_contact_person(supplier.contact_person)
        self.page.fill_contact_address(supplier.contact_address)
        self.page.fill_contact_number(supplier.contact_number)
        self.page.fill_email(supplier.email)

        self.page.click_add_item_button()
        self.page.fill_item_name(item.name, 1)
        self.page.fill_item_description(item.description, 1)
        self.page.select_brand_option(item.brand, 1)
        self.page.select_department_option(item.department, 1)
        self.page.select_category_option(item.category, 1)
        self.page.fill_selling_price(item.selling_price, 1)

        self.page.click_save_item_button()
