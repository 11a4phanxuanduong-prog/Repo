from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo Chrome (nếu bạn dùng ChromeDriver mới thì chỉ cần dòng này)
driver = webdriver.Chrome()

for i in range(65, 91):  # A → Z (ASCII 65 đến 90)
    url = f"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_{chr(i)}"

    try:
        print(f"\n===== ĐANG LẤY CHỮ {chr(i)} =====")
        
        # Mở trang
        driver.get(url)

        # Đợi trang tải
        time.sleep(2)

        # Lấy ra tất cả thẻ <ul>
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print("Số lượng UL tìm được:", len(ul_tags))

        # Kiểm tra xem có đủ ul để chọn ul thứ 21 không
        if len(ul_tags) <= 20:
            print("Không có UL thứ 21! Bỏ qua.")
            continue

        # Chọn UL thứ 21 (index 20)
        ul_painters = ul_tags[20]

        # Lấy tất cả li trong ul này
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Lấy tất cả tiêu đề nằm trong thẻ <a>
        titles = [
            tag.find_element(By.TAG_NAME, "a").get_attribute("title")
            for tag in li_tags
            if tag.find_elements(By.TAG_NAME, "a")  # tránh lỗi nếu li không có thẻ a
        ]

        # In kết quả
        for t in titles:
            print(t)

    except Exception as e:
        print("Lỗi:", e)

# Đóng trình duyệt
driver.quit()
