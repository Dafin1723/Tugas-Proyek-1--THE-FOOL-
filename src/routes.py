from flask import render_template, request, redirect, url_for, flash, send_from_directory, session, jsonify, send_file
from werkzeug.utils import secure_filename
from models import db, Pesanan, get_statistics
import os
from datetime import datetime
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

#(Dafin )
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return redirect(url_for('produk'))

@app.before_request
def require_admin_login():
    if request.path.startswith('/admin') and request.path != '/admin/login':
        if not session.get('admin_logged_in'):
            flash('Silakan login terlebih dahulu sebagai admin.', 'warning')
            return redirect(url_for('admin_login'))
