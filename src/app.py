from flask import Flask
from models import db, init_db
from routes import register_routes
import os
from pathlib import Path

app = Flask(__name__)


