import logging
import os
import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for, session

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.secret_key = 'secret123'  # Kunci sesi login admin

# Data login admin (sementara, nanti bisa pakai database)
ADMIN_CREDENTIALS = {
    "admin": "admin123"
}

# Fungsi koneksi ke database
def get_db_connection():
    conn = sqlite3.connect("pos.db")
    conn.row_factory = sqlite3.Row  # Supaya hasil query bisa diakses seperti dictionary
    return conn

# ✅ Halaman pertama yang muncul: Pilihan User atau Admin
@app.route("/")
def home():
    return render_template("home.html")

# ✅ Halaman User
@app.route("/user")
def user():
    return render_template("index.html")

@app.route("/product-list")
def product():
    return render_template("product-list.html")

@app.route("/product-detail")
def product_detail():
    return render_template("product-detail.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

# ✅ Halaman Login Admin
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session["admin"] = username  # Simpan sesi login
            return redirect(url_for("admin_dashboard"))
        else:
            return "Login gagal! Periksa kembali username & password."
    return render_template("admin_login.html")

# ✅ Dashboard Admin
@app.route("/admin-dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))  # Redirect ke login jika belum login
    return render_template("admin_dashboard.html")

# ✅ Logout Admin
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

# ✅ Menampilkan semua produk di dashboard
@app.route("/admin-products")
def admin_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM produk").fetchall()
    conn.close()
    return render_template("admin_products.html", products=products)

# ✅ Tambah produk baru
@app.route("/add-product", methods=["POST"])
def add_product():
    nama = request.form["nama"]
    harga = request.form["harga"]
    stok = request.form["stok"]
    
    conn = get_db_connection()
    conn.execute("INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)", (nama, harga, stok))
    conn.commit()
    conn.close()
    
    return redirect(url_for("admin_products"))

# ✅ Hapus produk
@app.route("/delete-product/<int:id>")
def delete_product(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM produk WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for("admin_products"))

# ✅ Menampilkan transaksi dengan JOIN untuk menampilkan nama produk
@app.route("/admin-transactions")
def transaksi():
    conn = get_db_connection()
    
    # Ambil daftar produk untuk form transaksi
    products = conn.execute("SELECT * FROM produk").fetchall()

    # Ambil transaksi yang bergabung dengan nama produk
    transactions = conn.execute("""
        SELECT transaksi.id, produk.nama AS nama_produk, transaksi.jumlah, transaksi.total_harga, transaksi.tanggal
        FROM transaksi
        JOIN produk ON transaksi.produk_id = produk.id
    """).fetchall()

    conn.close()
    return render_template("admin_transactions.html", transactions=transactions, products=products)

# ✅ Tambah transaksi
@app.route("/add-transaction", methods=["POST"])
def add_transaction():
    produk_id = request.form["produk_id"]
    jumlah = int(request.form["jumlah"])
    
    conn = get_db_connection()
    
    # Ambil harga dan stok produk
    produk = conn.execute("SELECT harga, stok FROM produk WHERE id = ?", (produk_id,)).fetchone()

    if not produk:
        conn.close()
        return "Produk tidak ditemukan!", 400

    harga_satuan = produk["harga"]
    total_harga = harga_satuan * jumlah
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simpan transaksi ke database
    conn.execute("INSERT INTO transaksi (produk_id, jumlah, total_harga, tanggal) VALUES (?, ?, ?, ?)",
                 (produk_id, jumlah, total_harga, tanggal))

    # Update stok produk
    new_stok = produk["stok"] - jumlah
    conn.execute("UPDATE produk SET stok = ? WHERE id = ?", (new_stok, produk_id))

    conn.commit()
    conn.close()

    return redirect(url_for("transaksi"))

# ✅ Jalankan aplikasi Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
