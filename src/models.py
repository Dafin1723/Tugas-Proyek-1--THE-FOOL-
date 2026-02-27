class Pesanan(db.Model):
    __tablename__ = 'pesanan'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Data customer
    nama = db.Column(db.String(100), nullable=False)
    kontak = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)  # NEW
    
    # Detail order
    jenis_print = db.Column(db.String(50), nullable=False)
    warna = db.Column(db.String(20), nullable=False)  # NEW: "Hitam Putih" atau "Berwarna"
    ukuran = db.Column(db.String(20), nullable=False)
    jenis_kertas = db.Column(db.String(50), nullable=False)  # NEW
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal_ambil = db.Column(db.String(20), nullable=False)  # NEW
    catatan = db.Column(db.Text, nullable=True)  # NEW
    
    # Files (store as JSON array)
    file_paths = db.Column(db.Text, nullable=True)  # NEW: JSON array of filenames
    
    # System
    nomor_antrian = db.Column(db.String(20), unique=True, nullable=False)  # NEW
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        import json
        
        # Parse file paths from JSON
        files = json.loads(self.file_paths) if self.file_paths else []
        
        return {
            'id': self.id,
            'nomor_antrian': self.nomor_antrian,
            'nama': self.nama,
            'kontak': self.kontak,
            'email': self.email,
            'jenis_print': self.jenis_print,
            'warna': self.warna,
            'ukuran': self.ukuran,
            'jenis_kertas': self.jenis_kertas,
            'jumlah': self.jumlah,
            'tanggal_ambil': self.tanggal_ambil,
            'catatan': self.catatan,
            'file_paths': files,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @property
    def status_indo(self):
        """Status dalam bahasa Indonesia"""
        status_map = {
            'pending': 'Menunggu',
            'proses': 'Diproses',
            'selesai': 'Selesai'
        }
        return status_map.get(self.status, self.status)
    
    @property
    def file_count(self):
        """Jumlah file yang diupload"""
        import json
        if not self.file_paths:
            return 0
        files = json.loads(self.file_paths)
        return len(files)
