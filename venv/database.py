import sqlite3

# Buat dan koneksi ke database
conn = sqlite3.connect("pos.db")
cursor = conn.cursor()

# Buat tabel Produk
cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga INTEGER NOT NULL,
    stok INTEGER NOT NULL
)
""")

# Buat tabel Transaksi
cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produk_id INTEGER,
    jumlah INTEGER NOT NULL,
    total_harga INTEGER NOT NULL,
    tanggal TEXT NOT NULL,
    FOREIGN KEY (produk_id) REFERENCES produk (id)
)
""")

conn.commit()
conn.close()
print("Database berhasil dibuat!")
