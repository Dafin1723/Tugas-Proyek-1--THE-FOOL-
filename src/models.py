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

      
    def __repr__(self):
        return f'<Pesanan {self.id}: {self.nama} - {self.jenis_print}>'
    
    def to_dict(self):
        """Convert model to dictionary untuk API response"""
        return {
            'id': self.id,
            'nama': self.nama,
            'kontak': self.kontak,
            'jenis_print': self.jenis_print,
            'ukuran': self.ukuran,
            'jumlah': self.jumlah,
            'file_path': self.file_path,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    @property
    def status_indo(self):
        """Get status dalam bahasa Indonesia"""
        status_map = {
            'pending': 'Menunggu',
            'proses': 'Diproses',
            'selesai': 'Selesai'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def status_color(self):
        """Get warna status untuk UI"""
        color_map = {
            'pending': 'warning',
            'proses': 'info',
            'selesai': 'success'
        }
        return color_map.get(self.status, 'secondary')


def init_db(app):
    """
    Initialize database dengan Flask app
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database initialized successfully!")

def get_statistics():
    """
    Get statistik pesanan untuk dashboard admin
    
    Returns:
        dict: Dictionary berisi statistik
    """
    total = Pesanan.query.count()
    pending = Pesanan.query.filter_by(status='pending').count()
    proses = Pesanan.query.filter_by(status='proses').count()
    selesai = Pesanan.query.filter_by(status='selesai').count()
    
    return {
        'total': total,
        'pending': pending,
        'proses': proses,
        'selesai': selesai
    }