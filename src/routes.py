import json
from datetime import datetime
import secrets

@app.route('/pesan', methods=['GET', 'POST'])
def pesan():
    if request.method == 'POST':
        try:
            nama = request.form.get('nama')
            kontak = request.form.get('kontak')
            email = request.form.get('email')
            jenis_print = request.form.get('jenis_print')
            warna = request.form.get('warna')
            ukuran = request.form.get('ukuran')
            jenis_kertas = request.form.get('jenis_kertas')
            jumlah = request.form.get('jumlah')
            tanggal_ambil = request.form.get('tanggal_ambil')
            catatan = request.form.get('catatan', '')

            if not all([nama, kontak, email, jenis_print, warna, ukuran, jenis_kertas, jumlah, tanggal_ambil]):
                return jsonify({
                    'success': False,
                    'message': 'Semua field wajib harus diisi!'
                }), 400

            files = request.files.getlist('files[]')
            uploaded_files = []
            
            if files and files[0].filename:
                if len(files) > 10:
                    return jsonify({
                        'success': False,
                        'message': 'Maksimal 10 file!'
                    }), 400

                for file in files:
                    if file and allowed_file(file.filename):
                        file.seek(0, os.SEEK_END)
                        file_length = file.tell()
                        if file_length > 20 * 1024 * 1024:  # 20MB
                            return jsonify({
                                'success': False,
                                'message': f'File {file.filename} terlalu besar! Maksimal 20MB.'
                            }), 400
                        file.seek(0)  # Reset file pointer

                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        unique_filename = f'{timestamp}_{filename}'
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                        file.save(file_path)
                        uploaded_files.append(unique_filename)

            # Store file paths as JSON array
            file_paths_json = json.dumps(uploaded_files) if uploaded_files else None

            # Generate nomor antrian (queue number)
            # Format: YYYYMMDD-XXX (date + sequential number)
            today = datetime.now().strftime('%Y%m%d')
            today_orders = Pesanan.query.filter(
                Pesanan.created_at >= datetime.now().date()
            ).count()
            nomor_antrian = f"{today}-{str(today_orders + 1).zfill(3)}"

            # Create new order
            pesanan_baru = Pesanan(
                nama=nama,
                kontak=kontak,
                email=email,
                jenis_print=jenis_print,
                warna=warna,
                ukuran=ukuran,
                jenis_kertas=jenis_kertas,
                jumlah=int(jumlah),
                tanggal_ambil=tanggal_ambil,
                catatan=catatan,
                file_paths=file_paths_json,
                nomor_antrian=nomor_antrian,
                status='pending'
            )

            db.session.add(pesanan_baru)
            db.session.commit()

            # Return success with queue number
            return jsonify({
                'success': True,
                'pesanan_id': pesanan_baru.id,
                'nomor_antrian': nomor_antrian,
                'message': 'Pesanan berhasil dibuat!'
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500

    return render_template('form-pemesanan-baru.html')


# Route baru untuk receipt page
@app.route('/receipt/<int:pesanan_id>')
def receipt(pesanan_id):
    """Receipt page dengan nomor antrian besar"""
    pesanan = Pesanan.query.get_or_404(pesanan_id)
    
    return render_template('receipt.html', pesanan=pesanan)


# Update allowed file function
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS