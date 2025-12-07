import sqlite3
# ket noi voi du lireu
conn = sqlite3.connect("inventory.db")
# tao doi tyuong  để thực thi các câu lệnh SQL
cur = conn.cursor()


sql1 = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity INTEGER
);
"""

# THUC thi cau lenhj
cur.execute(sql1)
conn.commit() # lua thay doi vao db

products_data = [
    ("laptop a100 ",25.50 ,50),
    ("asuvivobook" ,2293 ,44),
    ("dddd",666,44)
]
sql2 = """
INSERT INTO products (name, price, quantity)
VALUES (?, ?, ?)
"""
cur.executemany(sql2, products_data)
conn.commit()

# read
sql3 = "SELECT * FROM PRODUCTS"
# thuc thi trruy vaan

cur.execute(sql3)

#lay tat ca ket qua
all_products= cur.fetchall()

# in tieu dde
print(f"{'ID':<4}|{' tên sản phẩm':<20}|{'giá':<10}")
# lặp in ra
for p in all_products:
    print(f"{p[0]:<4} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10}")