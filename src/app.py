from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from pathlib import Path

# MODEL DATABASE
class Pesanan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kontak = db.Column(db.String(100))
    jenis_print = db.Column(db.String(50))
    ukuran = db.Column(db.String(20))
    jumlah = db.Column(db.Integer)
    file_path = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')

# Buat tabel (kalau belum ada)
with app.app_context():
    db.create_all()

# Halaman Katalog Produk (template produk.html)
@app.route('/produk')
def produk():
    return render_template('produk.html')

# Penggabungan di handle Dafin
