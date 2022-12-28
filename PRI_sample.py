from random import randint
from time import sleep
import pandas as pd
import undetected_chromedriver.v2 as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re

username = 'xxxxxxxxxx'
password = 'xxxxxxxxxx'

def main():
    print("Starting...")
    
    session = login(open_driver())
    sleep(randint(5,10))
    session.quit()


def open_driver(option="Yes"):
    """
    Opens chrome browser, sets visibility options (default is visible) and returns driver
    """
    print("Opening Chrome...")

    if option == "Yes":
        driver = uc.Chrome()
        return driver
    elif option == "No":
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = uc.Chrome(options=chrome_options)
        return driver

def login(driver):
    """
    Logs into the website, returns logged in session
    """
    print("Logging into the Website...")

    driver.get("https://pip2022.unpri.org/pip/login.aspx")
    sleep(randint(2,5))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Login to website
    driver.find_element(By.XPATH, "//*[@id='txtLoginEmail']").send_keys(username)
    sleep(randint(2,7))
    driver.find_element(By.XPATH, "//*[@id='txtLoginPassword']").send_keys(password)
    sleep(randint(2,4))
    driver.find_element(By.ID, 'loginButton').click()  
    print("Registration Complete\n")
    sleep(randint(3,5))

    # Go to a certain page
    if driver.current_url == 'https://pip2022.unpri.org/pip/registration/':
        driver.get('xxxxxxxxxxxxx')
        scrape(driver)
        return driver

def scrape(driver):
    """"
    Scrape the webpage and use the search bar
    """
    print("Getting Contact Info...\n")
    contacts = ["xxxxxx", "xxxxxxx", "xxxxxxx....."]
    output = []
    for contact in contacts:
        # Click the first image
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.image'))))
        
        # Extract info from the window image
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.bootbox-body')))
        name = driver.find_element(By.CSS_SELECTOR, "div[class='modal-text'] h2").text
        positions = driver.find_element(By.CSS_SELECTOR, 'p.position').text
        position, company_name = re.split(',+', positions)
        company = company_name.lstrip()
        info = {'Name': name,
        'Job Title': position,
        'Company': company, }
        output.append(info)
        print(f"{name} extracted.\n")
        sleep(randint(3,5))
        
        # Exit the window
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[onclick='closePopoverModal()'] i[class='fas fa-times fa-stack-1x delegate-speaker-modal-icon']"))).click()
        
        # Use search bar
        driver.find_element(By.CSS_SELECTOR,'#ctl00_PageContent_txtSearchTerms').clear()
        sleep(randint(1,2))
        driver.find_element(By.CSS_SELECTOR,'#ctl00_PageContent_txtSearchTerms').send_keys(contact)
        sleep(randint(2,4))
        # Search for the next contact
        driver.find_element(By.CSS_SELECTOR,"i[class='fa fa-search']").click()
    print('----------- Extraction Complete -----------')
    
    # Save file to a format
    df = pd.DataFrame(output)
    df.to_csv('event_contacts.csv')
    print('saved to file')


if __name__ == "__main__":
    main()

#list > div:nth-child(1)
#list > div:nth-child(1)
# /html/body/form/div[3]/div/div/div/div[2]/div[2]/div[1]
#  driver.find_element(By.CSS_SELECTOR, '.delegates-list-item hotlink') .click()

# search_result = driver.find_element(By.ID, 'results')
# # delegates = search_result.find_element(By.CSS_SELECTOR, '.delegates-list')
# delegates.find_element(By.CSS_SELECTOR, '.delegates-list-item hotlink').click()