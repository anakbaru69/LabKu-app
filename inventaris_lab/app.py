# import os
# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for, flash
# import pandas as pd

# app = Flask(__name__)
# app.secret_key = 'secret_key_anda'
# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# EXCEL_FILE = 'data.xlsx'

# # Pastikan folder upload ada
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Inisialisasi file Excel jika belum ada
# if not os.path.exists(EXCEL_FILE):
#     df = pd.DataFrame(columns=[
#         'Tipe', 'Nama', 'NIM', 'Nama Barang', 'Foto Barang', 'Waktu'
#     ])
#     df.to_excel(EXCEL_FILE, index=False)

# def save_to_excel(data):
#     df = pd.read_excel(EXCEL_FILE)
#     df = df._append(data, ignore_index=True)
#     df.to_excel(EXCEL_FILE, index=False)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/pinjam', methods=['GET', 'POST'])
# def pinjam():
#     if request.method == 'POST':
#         nama = request.form['nama']
#         nim = request.form['nim']
#         nama_barang = request.form['nama_barang']
#         waktu = request.form['waktu']

#         # Handle foto upload
#         foto = request.files['foto']
#         if foto.filename == '':
#             flash('Foto barang harus diupload')
#             return redirect(request.url)
#         foto_filename = datetime.now().strftime("%Y%m%d%H%M%S_") + foto.filename
#         foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

#         data = {
#             'Tipe': 'Pinjam',
#             'Nama': nama,
#             'NIM': nim,
#             'Nama Barang': nama_barang,
#             'Foto Barang': foto_filename,
#             'Waktu': waktu
#         }
#         save_to_excel(data)
#         flash('Data peminjaman berhasil disimpan')
#         return redirect(url_for('index'))

#     return render_template('pinjam.html')

# @app.route('/kembalikan', methods=['GET', 'POST'])
# def kembalikan():
#     if request.method == 'POST':
#         nama = request.form['nama']
#         nim = request.form['nim']
#         nama_barang = request.form['nama_barang']
#         waktu = request.form['waktu']

#         # Handle foto upload
#         foto = request.files['foto']
#         if foto.filename == '':
#             flash('Foto barang harus diupload')
#             return redirect(request.url)
#         foto_filename = datetime.now().strftime("%Y%m%d%H%M%S_") + foto.filename
#         foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

#         data = {
#             'Tipe': 'Kembalikan',
#             'Nama': nama,
#             'NIM': nim,
#             'Nama Barang': nama_barang,
#             'Foto Barang': foto_filename,
#             'Waktu': waktu
#         }
#         save_to_excel(data)
#         flash('Data pengembalian berhasil disimpan')
#         return redirect(url_for('index'))

#     return render_template('kembalikan.html')

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)






# app.py
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'secret_key_anda')

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

EXCEL_FILE = os.path.join(app.root_path, 'data.xlsx')

# init excel if not exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Tipe', 'Nama', 'NIM', 'Nama Barang', 'Foto Barang', 'Waktu'])
    df.to_excel(EXCEL_FILE, index=False)

def save_to_excel(data):
    # baca dan tambahkan baris
    df = pd.read_excel(EXCEL_FILE)
    df = df._append(data, ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # endpoint untuk menampilkan file foto (opsional)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/pinjam', methods=['GET', 'POST'])
def pinjam():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        nama_barang = request.form['nama_barang']
        waktu = request.form['waktu']
        foto = request.files.get('foto')

        if not foto or foto.filename == '':
            flash('Foto barang harus diupload')
            return redirect(request.url)

        foto_filename = datetime.now().strftime("%Y%m%d%H%M%S_") + secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

        data = {
            'Tipe': 'Pinjam',
            'Nama': nama,
            'NIM': nim,
            'Nama Barang': nama_barang,
            'Foto Barang': foto_filename,
            'Waktu': waktu
        }
        save_to_excel(data)
        flash('Data peminjaman berhasil disimpan')
        return redirect(url_for('index'))

    return render_template('pinjam.html')

@app.route('/kembalikan', methods=['GET', 'POST'])
def kembalikan():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        nama_barang = request.form['nama_barang']
        waktu = request.form['waktu']
        foto = request.files.get('foto')

        if not foto or foto.filename == '':
            flash('Foto barang harus diupload')
            return redirect(request.url)

        foto_filename = datetime.now().strftime("%Y%m%d%H%M%S_") + secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

        data = {
            'Tipe': 'Kembalikan',
            'Nama': nama,
            'NIM': nim,
            'Nama Barang': nama_barang,
            'Foto Barang': foto_filename,
            'Waktu': waktu
        }
        save_to_excel(data)
        flash('Data pengembalian berhasil disimpan')
        return redirect(url_for('index'))

    return render_template('kembalikan.html')

if __name__ == '__main__':
    # listen di 0.0.0.0 agar dapat diakses dari luar
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug)
