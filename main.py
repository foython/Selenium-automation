import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
user_data_dir = r'C:\Users\Ahyan\AppData\Local\Google\Chrome\User Data\Default'
chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_driver_path = './chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Link and name of CSV
driver.get("https://app.apollo.io/#/people?finderViewId=5b8050d050a3893c382e9360&organizationIndustryTagIds[]=5567cd477369645401010000&page=1")
csv_file_name = 'RealEstate.csv'

time.sleep(10)

def split_name(name):
    parts = name.split() 
    first_name = parts[0] if parts else ''
    last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    return first_name, last_name


while True:
    print("Current URL:", driver.current_url)
    
    try:
        loaded_section_selector = "[data-cy-loaded='true']"
        loaded_section = driver.find_element(By.CSS_SELECTOR, loaded_section_selector)

        tbodies = loaded_section.find_elements(By.TAG_NAME, 'tbody')
        if not tbodies:
            break

        for tbody in tbodies:
            td_list = tbody.find_elements(By.TAG_NAME, 'td')
            if td_list:
                name= td_list[0].text
                first_name, last_name = split_name(name)
                job_title = td_list[1].text
                company_name= td_list[2].text
                contact_ocation = td_list[4].text
                employees = td_list[5].text
                industry = td_list[7].text
           
            linkedin_url = ''
            for link in tbody.find_elements(By.TAG_NAME, 'a'):
                href = link.get_attribute('href')
                if 'linkedin.com' in href:
                    linkedin_url = href
                    break
                          
            phone_number = ''
                       
            try:
                button = tbody.find_element(By.CSS_SELECTOR, '.zp_zUY3r.zp_n9QPr.zp_MCSwB')
                
                if button:
                    button.click()
                    time.sleep(1)
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME,'zp_t08Bv'))
    )
                    email_addresses = element.text
                    
                    verified =  driver.find_element(By.CSS_SELECTOR,'.zp_tDE3F.zp_SxO7r').text
                    if verified == 'Email is Verified':
                        verified = 'Verified'
                    else:
                        verified = 'Not Verified'
                    
                    chatBox = driver.find_element(By.CSS_SELECTOR, '.zp_YI5xm')
                    driver.execute_script("arguments[0].remove();", chatBox)                                   
                    time.sleep(2)
                    phone_number = tbody.find_element(By.CSS_SELECTOR, '.zp-link.zp_OotKe.zp_vc37T').text 

                    with open(csv_file_name, 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        print(f"{first_name} has been poached!")                       
                        writer.writerow([first_name, last_name, job_title, company_name, linkedin_url, email_addresses, verified, phone_number, contact_ocation, employees, industry]) 
                    print(f'first_name: {first_name}, last_name: {last_name}, job: {job_title}, email: {email_addresses} contact:{phone_number} {verified}' )              
                            
            except NoSuchElementException:
                print('no button found')
                continue

        # Pagination Logic
        next_button_selector = ".zp-button.zp_zUY3r.zp_MCSwB.zp_xCVC8[aria-label='right-arrow']"
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, next_button_selector)
            next_button.click()
            time.sleep(3)
        except NoSuchElementException:
            print("No more pages to navigate.")
            break

    except Exception as e:
        error_message = str(e)
        if "element click intercepted" in error_message:
            print("Your leads are ready!")
            break
        else:
            print(f"An error occurred: {error_message}")
            break

driver.quit()