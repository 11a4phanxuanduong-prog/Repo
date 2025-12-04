import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


url = "https://en.wikipedia.org/wiki/List_of_universities_in_Vietnam"

service = Service(r'C:\Users\asus\OneDrive\Desktop\Selendium\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get(url)

tables = driver.find_elements(By.CLASS_NAME, "wikitable")
dfs = []

for i, table in enumerate(tables, 1):
    heading_elements = table.find_elements(By.XPATH, f"({" | ".join(f"preceding::h{i}" for i in range(2, 7))})[last()]")
    if heading_elements:
        heading = heading_elements[0].text
    else:
        heading = f"No heading found ({i})"

    trs = table.find_elements(By.TAG_NAME, 'tr')
    columns = [re.sub(r"hide\n", "", th.text.strip()) for th in trs[0].find_elements(By.TAG_NAME, 'th')]
    lenght = len(columns)
    
    data = []
    rowspan_tracker = {}

    for tr in trs[1:]:
        row = []
        cells = tr.find_elements(By.CSS_SELECTOR, 'td, th')
        col_index = 0

        while col_index < len(columns):
            if col_index in rowspan_tracker:
                row.append(rowspan_tracker[col_index][0])
                rowspan_tracker[col_index][1] -= 1
                if rowspan_tracker[col_index][1] == 0:
                    del rowspan_tracker[col_index]
                col_index += 1
                continue

            if cells:
                cell = cells.pop(0)
                row.append(cell.text.strip())
                rowspan = cell.get_attribute('rowspan')
                if rowspan and int(rowspan) > 1:
                    rowspan_tracker[col_index] = [cell.text.strip(), int(rowspan) - 1]
            else:
                row.append('')
            col_index += 1

        data.append(row)
        
    df = pd.DataFrame(data, columns=columns)
    dfs.append([heading, df])

with pd.ExcelWriter('all_university.xlsx') as writer:
    for heading, df in dfs:
        valid_sheet_name = re.sub(r'[\\/*?:"<>|]', "_", heading)[:31]
        df.to_excel(writer, sheet_name=valid_sheet_name, index=False)

driver.quit()