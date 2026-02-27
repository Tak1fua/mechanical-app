from playwright.sync_api import sync_playwright

def verify_app():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 1. Visit Home
        page.goto("http://127.0.0.1:5000/")
        page.screenshot(path="verification_home.png")
        print("Visited Home")

        # 2. Add Company
        page.click("text=Empresas")
        page.fill("input[name='name']", "Taller Juan")
        page.fill("input[name='tax_id']", "999-888")
        page.fill("input[name='contact_info']", "juan@taller.com")
        page.click("button:has-text('Guardar')")
        page.screenshot(path="verification_companies.png")
        print("Added Company")

        # 3. Add Vehicle
        page.click("text=Vehículos")
        page.fill("input[name='plate']", "ZZZ-111")
        page.fill("input[name='make']", "Chevrolet")
        page.fill("input[name='model']", "Sail")
        page.fill("input[name='year']", "2022")
        page.select_option("select[name='company_id']", label="Taller Juan")
        page.click("button:has-text('Guardar')")
        page.screenshot(path="verification_vehicles.png")
        print("Added Vehicle")

        # 4. Add Service History
        page.click("text=Ver Historial") # Click on the first vehicle's history link
        page.fill("input[name='date']", "2023-11-15")
        page.fill("textarea[name='description']", "Mantenimiento General")
        page.fill("input[name='cost']", "150.00")
        page.click("button:has-text('Agregar Servicio')")
        page.screenshot(path="verification_history.png")
        print("Added Service History")
        
        browser.close()

if __name__ == "__main__":
    verify_app()
