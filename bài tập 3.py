
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd

# 1. Setup Selenium

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

url = "https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/vitamin-khoang-chat"
driver.get(url)

# 2. Setup SQLite

DB_FILE = 'longchau_db.sqlite'

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Đã xóa file DB cũ: {DB_FILE}")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    price INTEGER,
    unit TEXT,
    original_price INTEGER,
    product_url TEXT UNIQUE
)
""")

conn.commit()

# 3. Hàm lưu dữ liệu tức thời

def save_product(data):
    cursor.execute("""
        INSERT OR IGNORE INTO products (product_name, price, unit, original_price, product_url)
        VALUES (?, ?, ?, ?, ?)
    """, data)
    conn.commit()

# 4. Bắt đầu cào dữ liệu

while True:
    try:
        btn = driver.find_element(By.CSS_SELECTOR, "button.mt-3")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
    except:
        break

for product in driver.find_elements(By.CSS_SELECTOR, "div.px-4 > div.grid > div.h-full"):
    # Lấy tên sản phẩm với xử lý lỗi
    try:
        product_name = product.find_element(By.CSS_SELECTOR, "h3.overflow-hidden").text
        product_name = product_name if product_name else None
    except:
        product_name = None

    # Lấy giá sản phẩm và loại bỏ ký tự không cần thiết
    try:
        price = product.find_element(By.CSS_SELECTOR, "div.text-blue-5 > span.font-semibold").text
        price = price.replace(".", "").replace("đ", "").strip()
    except:
        price = None

    # Lấy đơn vị giá, đảm bảo có ít nhất 2 phần tử sau khi split
    try:
        unit = product.find_element(By.CSS_SELECTOR, "div.text-blue-5 > span.text-label2").text.split()
        unit = unit[1] if len(unit) > 1 else None
    except:
        unit = None

    # Lấy giá gốc và xử lý ký tự không cần thiết
    try:
        original_price = product.find_element(By.CSS_SELECTOR, "div.font-normal.text-gray-6").text
        original_price = original_price.replace(".", "").replace("đ", "").strip()
    except:
        original_price = price

    # Lấy URL sản phẩm
    try:
        product_url = product.find_element(By.CSS_SELECTOR, "a.block.px-3").get_attribute("href")
    except:
        product_url = None

    save_product([product_name, price, unit, original_price, product_url])

driver.quit()
print("Save Success!")

conn.close()

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("\n===== NHÓM 1: KIỂM TRA CHẤT LƯỢNG DỮ LIỆU =====")

# 1. Kiểm tra trùng lặp theo product_url
print("\n1. Trùng lặp product_url:")
cursor.execute("""
SELECT product_url, COUNT(*)
FROM products
GROUP BY product_url
HAVING COUNT(*) > 1
""")
print(cursor.fetchall())

# 2. Kiểm tra trùng lặp theo product_name
print("\n2. Trùng lặp product_name:")
cursor.execute("""
SELECT product_name, COUNT(*)
FROM products
GROUP BY product_name
HAVING COUNT(*) > 1
""")
print(cursor.fetchall())

# 3. Dữ liệu thiếu giá
print("\n3. Sản phẩm không có giá:")
cursor.execute("SELECT COUNT(*) FROM products WHERE price IS NULL OR price = 0")
print(cursor.fetchone()[0])

# 4. Liệt kê unit duy nhất
print("\n4. Danh sách đơn vị tính:")
cursor.execute("SELECT DISTINCT unit FROM products")
print(cursor.fetchall())

# 5. Tổng số bản ghi
print("\n5. Tổng số lượng sản phẩm:")
cursor.execute("SELECT COUNT(*) FROM products")
print(cursor.fetchone()[0])


print("\n===== NHÓM 2: KHẢO SÁT VÀ PHÂN TÍCH =====")

# 6. 10 sản phẩm giá cao nhất
print("\n6. 10 sản phẩm đắt nhất:")
cursor.execute("""
SELECT product_name, price FROM products 
ORDER BY price DESC LIMIT 10
""")
print(cursor.fetchall())

# 7. Sản phẩm có giá cao nhất
print("\n7. Sản phẩm giá cao nhất:")
cursor.execute("""
SELECT product_name, price FROM products 
ORDER BY price DESC LIMIT 1
""")
print(cursor.fetchone())

# 8. Đếm số lượng theo đơn vị
print("\n8. Số lượng theo đơn vị:")
cursor.execute("""
SELECT unit, COUNT(*) FROM products 
GROUP BY unit
""")
print(cursor.fetchall())

# 9. Tìm sản phẩm chứa từ 'Vitamin C'
print("\n9. Sản phẩm chứa 'Vitamin C':")
cursor.execute("""
SELECT * FROM products 
WHERE product_name LIKE '%Vitamin C%'
""")
print(cursor.fetchall())

# 10. Lọc theo khoảng giá
print("\n10. Sản phẩm từ 100k - 200k:")
cursor.execute("""
SELECT product_name, price FROM products 
WHERE price BETWEEN 100000 AND 200000
""")
print(cursor.fetchall())


print("\n===== NHÓM 3: NÂNG CAO =====")

# 11. Sắp xếp theo giá tăng dần
print("\n11. Sắp xếp theo giá tăng dần:")
cursor.execute("""
SELECT product_name, price FROM products 
ORDER BY price ASC
""")
print(cursor.fetchall())

# 12. Gom nhóm theo mức giá
print("\n12. Thống kê theo nhóm giá:")
cursor.execute("""
SELECT
    CASE 
        WHEN price < 50000 THEN 'Dưới 50k'
        WHEN price BETWEEN 50000 AND 100000 THEN '50k - 100k'
        ELSE 'Trên 100k'
    END AS price_group,
    COUNT(*)
FROM products
GROUP BY price_group
""")
print(cursor.fetchall())

# 13. URL rỗng hoặc NULL
print("\n13. URL không hợp lệ:")
cursor.execute("""
SELECT * FROM products WHERE product_url IS NULL OR product_url = ''
""")
print(cursor.fetchall())

# 14. Xóa bản ghi trùng lặp (giữ id nhỏ nhất)
print("\n14. Xóa bản ghi trùng lặp theo product_name (mô phỏng):")
cursor.execute("""
DELETE FROM products
WHERE id NOT IN (
    SELECT MIN(id)
    FROM products
    GROUP BY product_name
)
""")
conn.commit()
print("Đã xóa bản ghi trùng lặp.")

# 15. Kiểm tra lại số lượng sau khi xóa
print("\n15. Tổng số bản ghi sau khi làm sạch:")
cursor.execute("SELECT COUNT(*) FROM products")
print(cursor.fetchone()[0])

conn.close()
