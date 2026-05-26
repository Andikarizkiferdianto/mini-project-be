import falcon
import os
import subprocess
from datetime import datetime
from models.schema import db
from pony.orm import db_session


class BackupDataResource:
    def on_get(self, req, resp):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_backups = os.path.join(base_dir, "backups")
        if not os.path.exists(folder_backups): os.makedirs(folder_backups)
        files = [f for f in os.listdir(folder_backups) if f.endswith('.sql')]
        resp.media = {"files": sorted(files, reverse=True)}

    @db_session
    def on_post(self, req, resp):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            folder_backups = os.path.join(base_dir, "backups")
            if not os.path.exists(folder_backups): os.makedirs(folder_backups)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nama_file = f"backup__{timestamp}.sql"
            path_lengkap = os.path.join(folder_backups, nama_file)

            # Path XAMPP
            mysqldump = r"C:\xampp\mysql\bin\mysqldump.exe"
            if not os.path.exists(mysqldump):
                mysqldump = r"C:\Users\WINDOWS\Desktop\xaammpp\mysql\bin\mysqldump.exe"

            cmd = f'"{mysqldump}" -u root --result-file="{path_lengkap}" sap_database'
            subprocess.run(cmd, shell=True, check=True)

            resp.media = {"status": "success", "message": "Backup berhasil"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}