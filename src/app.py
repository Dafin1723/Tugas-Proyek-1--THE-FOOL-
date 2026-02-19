from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from pathlib import Path

def pesan():
    if request.method == 'POST':
        nama = request.form.get('nama')
        kontak = request.form.get('kontak')
        jenis = request.form.get('jenis_print')
        ukuran = request.form.get('ukuran')
        jumlah = request.form.get('jumlah', type=int)
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            pesanan = Pesanan(nama=nama, kontak=kontak, jenis_print=jenis,
                              ukuran=ukuran, jumlah=jumlah, file_path=file_path)
            db.session.add(pesanan)
            db.session.commit()
            flash('Pesanan berhasil dikirim! Tunggu admin cek ya.', 'success')
        else:
            flash('File tidak valid atau kosong.', 'danger')
        return redirect(url_for('pesan'))
    return render_template('user/index.html')  # atau pesan.html kalau ganti nama

def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'unitproduksi123':
            session['admin_logged_in'] = True
            session['admin_user'] = username
            flash('Login berhasil! Selamat datang Admin.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('admin/login.html')

def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_user', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('admin_login'))

