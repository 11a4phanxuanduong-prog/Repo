import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# Khởi tạo driver

url = "https://en.wikipedia.org/wiki/List_of_universities_in_Vietnam"
service = Service(r"C:\Users\asus\OneDrive\Desktop\Selendium\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(url)


# Lấy tất cả các bảng
# --------------------------------------------------
tables = driver.find_elements(By.CSS_SELECTOR, "table.wikitable")
result = []

def find_table_heading(table):
    """Tìm heading gần nhất phía trên bảng"""
    heading_tags = table.find_elements(
        By.XPATH,
        "preceding::h2[1] | preceding::h3[1] | preceding::h4[1] | preceding::h5[1] | preceding::h6[1]"
    )
    return heading_tags[-1].text if heading_tags else "Unknown Heading"


# Xử lý từng bảng

for idx, table in enumerate(tables, 1):
    heading = find_table_heading(table)

    rows = table.find_elements(By.TAG_NAME, "tr")
    headers = [th.text.replace("hide\n", "").strip() for th in rows[0].find_elements(By.TAG_NAME, "th")]

    data = []
    rowspan_buffer = {}

    # Dò từng hàng

    for row in rows[1:]:
        row_data = []
        cells = row.find_elements(By.CSS_SELECTOR, "td, th")
        col = 0

        while col < len(headers):

            # Nếu cột đang bị rowspan từ hàng trên
            if col in rowspan_buffer:
                row_data.append(rowspan_buffer[col][0])
                rowspan_buffer[col][1] -= 1
                if rowspan_buffer[col][1] == 0:
                    del rowspan_buffer[col]
                col += 1
                continue

            # Nếu vẫn còn cell để pop
            if cells:
                cell = cells.pop(0)
                text = cell.text.strip()
                row_data.append(text)

                span = cell.get_attribute("rowspan")
                if span and int(span) > 1:
                    rowspan_buffer[col] = [text, int(span) - 1]

            else:
                row_data.append("")

            col += 1

        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    result.append([heading, df])


# Ghi ra file Excel
with pd.ExcelWriter("all_university.xlsx") as writer:
    for heading, df in result:
        sheet = re.sub(r'[\\/*?:"<>|]', "_", heading)[:31]
        df.to_excel(writer, sheet_name=sheet, index=False)

driver.quit()
