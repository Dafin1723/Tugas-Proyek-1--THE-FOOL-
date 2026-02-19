from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pesanan(db.Model):
    """
    Model untuk menyimpan data pesanan
    
    Columns:
        id: Primary key, auto increment
        nama: Nama pemesan
        kontak: Nomor kontak (HP/email)
        jenis_print: Jenis layanan (Document Print, T-Shirt, Mug, dll)
        ukuran: Ukuran kertas/produk (A4, A3, dll)
        jumlah: Jumlah pesanan
        file_path: Path file yang diupload
        status: Status pesanan (pending/proses/selesai)
        created_at: Timestamp pembuatan pesanan
    """
    
    __tablename__ = 'pesanan'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kontak = db.Column(db.String(100), nullable=False)
    jenis_print = db.Column(db.String(50), nullable=False)
    ukuran = db.Column(db.String(20), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending, proses, selesai
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    