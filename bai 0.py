from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

service = Service(r'C:\Users\asus\OneDrive\Desktop\Selendium\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get("https://gomotungkinh.com/")
time.sleep(2)

try:
    while True:
        driver.find_element(By.ID, "bonk").click()
        print(1)
        time.sleep(2)
except:
    driver.close()