from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

service = Service(r'C:\Users\asus\OneDrive\Desktop\Selendium\chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https:\\en.wikipedia.org/wiki/list_of_painters_by_name"
driver.get(url)

driver.maximize_window()

time.sleep(2)

tags = driver.find_elements(By.XPATH, "//a[contains(@title, 'List of painters')]")
links = [tag.get_attribute("href") for tag in tags]

for link in links:
    print(link)

driver.quit()