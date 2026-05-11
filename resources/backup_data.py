import falcon
import os
import subprocess
from datetime import datetime
from models.schema import db
from pony.orm import db_session


class BackupDataResource:
    @db_session
    def on_post(self, req, resp):
        try:
            # 1. Pastikan folder backups ada di folder project
            # Kita pakai path absolut biar gak bingung
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            folder_backups = os.path.join(base_dir, "backups")

            if not os.path.exists(folder_backups):
                os.makedirs(folder_backups)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nama_file = f"backup__{timestamp}.sql"
            path_lengkap = os.path.join(folder_backups, nama_file)

            # 2. PATH MYSQLDUMP - PASTIIN INI BENER DI LAPTOP KAMU
            # Ganti C: jadi D: kalau XAMPP kamu di D
            mysqldump = r"C:\xampp\mysql\bin\mysqldump.exe"

            if not os.path.exists(mysqldump):
                # Cek alternatif di D
                mysqldump = r"C:\Users\WINDOWS\Desktop\xaammpp\mysql\bin\mysqldump.exe"

                # Perintahnya tetap sama
                cmd = f'"{mysqldump}" -u root --result-file="{path_lengkap}" sap_database'

            print(f"DEBUG: Menjalankan command: {' '.join(cmd)}")  # Cek ini di terminal PyCharm!

            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

            # 4. Cek hasil
            if os.path.exists(path_lengkap) and os.path.getsize(path_lengkap) > 0:
                db.execute("INSERT INTO riwayat_backup (nama_file, path_file) VALUES ($n, $p)",
                           {"n": nama_file, "p": path_lengkap})
                resp.media = {"status": "success", "message": "DONE! Cek folder backups sekarang bro."}
            else:
                error_info = result.stderr if result.stderr else "File 0 KB"
                raise Exception(f"Gagal isi data: {error_info}")

        except Exception as e:
            print(f"ERROR BACKUP: {str(e)}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}