from flask import Flask
from models import db, init_db
from routes import register_routes
import os
from pathlib import Path

app = Flask(__name__)


app.secret_key = 'fikri-production-secret-key-2025'  

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)