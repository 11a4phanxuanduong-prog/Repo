from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# Khởi tạo Webdriver
all_links = []
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})
driver = webdriver.Chrome()

# I. Lấy danh sách link hoạ sĩ
for i in range(65, 91):
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    try:
        driver.get(url)
        time.sleep(3)

        ul_tags = driver.find_elements(By.TAG_NAME, "ul")

        # chọn đúng UL chứa danh sách hoạ sĩ
        ul_painters = ul_tags[20]

        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # lấy link
        for tag in li_tags:
            link = tag.find_element(By.TAG_NAME, "a").get_attribute("href")
            all_links.append(link)

    except:
        print("Error!")

driver.quit()

# II. Lấy thông tin chi tiết từng hoạ sĩ
count = 0
for link in all_links:
    if count > 3:         # demo lấy 4 người
        break
    count += 1

    try:
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(2)

        # name
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # birth
        try:
            birth_text = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td").text
            match = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth_text)
            birth = match[0] if match else ""
        except:
            birth = ""

        # death
        try:
            death_text = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td").text
            match = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death_text)
            death = match[0] if match else ""
        except:
            death = ""

        # nationality
        try:
            nationality = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td").text
        except:
            nationality = ""

        painter = {
            'name': name,
            'birth': birth,
            'death': death,
            'nationality': nationality
        }

        d = pd.concat([d, pd.DataFrame([painter])], ignore_index=True)

        driver.quit()

    except:
        pass

# III. Xuất file
file_name = 'Painters.xlsx'
d.to_excel(file_name, index=False)
print("Excel created:", file_name)
print(d)

import os
print("File saved to:", os.path.abspath("Painters.xlsx"))

