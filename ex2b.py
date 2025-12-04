from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
options.headless = False

ser = Service(r"C:\Users\asus\OneDrive\Desktop\Selendium\geckodriver.exe")
driver = webdriver.Firefox(options=options, service=ser)

url = 'https://gochek.vn/collections/all?sort_by=title-ascending'
driver.get(url)
time.sleep(2)

# CUỘN ĐÚNG CÁCH ĐỂ LOAD SẢN PHẨM
last = 0
while True:
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(1.5)
    new = driver.execute_script("return document.body.scrollHeight")
    if new == last:
        break
    last = new

time.sleep(2)

products = driver.find_elements(By.CSS_SELECTOR, "div.product-block.product-resize.site-animation")

print("Tổng sản phẩm tìm được:", len(products))

stt = []
ten_san_pham = []
gia_ban = []
giam_giasp = []
hinh_anh = []

for i, sp in enumerate(products, 1):

    # Tên sản phẩm
    try:
        tsp = sp.find_element(By.CSS_SELECTOR, "h3.pro-name a").text
    except:
        tsp = ""

    # Giá bán (giá sale)
    try:
        gsp = sp.find_element(By.CSS_SELECTOR, ".box-pro-prices .price").text
    except:
        gsp = ""

    # Giá gốc (nếu có)
    try:
        ggsp = sp.find_element(By.CSS_SELECTOR, ".box-pro-prices .compare-price").text
    except:
        ggsp = ""

    # Hình ảnh
    try:
        ha = sp.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    except:
        ha = ""

    if tsp.strip() != "":
        stt.append(i)
        ten_san_pham.append(tsp)
        gia_ban.append(gsp)
        giam_giasp.append(ggsp)
        hinh_anh.append(ha)
# Tạo df
df=pd.DataFrame({
    "STT" : stt,
    "Tên sản phẩm": ten_san_pham,
    "Giá bán":gia_ban,
    "giảm giá sản phẩm":giam_giasp,
    "Hình ảnh":hinh_anh
    
})

df.to_excel('tat_ca_sp_Gochek.xlsx', index=False)

print("✔ Xuất Excel thành công!")

