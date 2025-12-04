from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import time
import pandas as pd

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
# Đường dẫn đến file thực thi geckodriver

gecko_path = r"C:\Users\asus\OneDrive\Desktop\Selendium\geckodriver.exe"
# Khởi tởi đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options();
options.binary_location =r"C:\Program Files\Mozilla Firefox\firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options = options, service=ser)



# Tạo url
url = 'https://sso.hutech.edu.vn/login'

# Truy cập
driver.get(url)

# Tạm dừng khoảng 2 giây
time.sleep(2)



name_input = driver.find_element(By.XPATH, "//input[@name='username']")
password = driver.find_element(By.XPATH, "//input[@id='input_password_1']")
time.sleep(2)
name_input.send_keys('2386400966')

password.send_keys("mRwmMamC9X7s7@Y")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "label[for='SINHVIEN_DAIHOC']").click()
time.sleep(2)
login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn btn-primary waves-effect waves-themed w-100')]")
login_button.click()







time.sleep(5)

#driver.quit()