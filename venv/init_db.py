import sqlite3

# Koneksi ke database (akan membuat pos.db jika belum ada)
conn = sqlite3.connect('pos.db')
cursor = conn.cursor()

# Buat tabel produk jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga INTEGER NOT NULL,
    stok INTEGER NOT NULL
)
''')

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

# Simpan perubahan dan tutup koneksi
conn.commit()
conn.close()

print("Tabel 'produk' berhasil dibuat atau sudah ada!")
