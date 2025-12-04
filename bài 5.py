from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo driver
driver = webdriver.Chrome()

for i in range(65, 91):  # A -> Z
    url = f"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_{chr(i)}"

    try:
        print(f"\n===== LẤY DỮ LIỆU CHỮ {chr(i)} =====")
        
        driver.get(url)
        time.sleep(2)

        # Tìm tất cả thẻ <ul>
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print("Số lượng UL:", len(ul_tags))

        # Kiểm tra có đủ để chọn UL thứ 21 hay không
        if len(ul_tags) <= 20:
            print("Không tìm thấy UL thứ 21. Bỏ qua.")
            continue

        ul_painters = ul_tags[20]

        # Lấy các <li>
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Lấy title trong thẻ <a>
        titles = []
        for tag in li_tags:
            a_tags = tag.find_elements(By.TAG_NAME, "a")
            if a_tags:  
                titles.append(a_tags[0].get_attribute("title"))

        # In kết quả
        for title in titles:
            print(title)

    except Exception as e:
        print("Error:", e)

# Đóng trình duyệt
driver.quit()
