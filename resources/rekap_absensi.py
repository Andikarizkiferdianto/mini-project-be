import falcon
from models.schema import db
from pony.orm import db_session


class RekapAbsensiResource:
    @db_session
    def on_get(self, req, resp):
        try:
            cursor = db.execute("SHOW TABLES")
            daftar_tabel = [list(row)[0] for row in cursor]

            tabel_terkait = [t for t in daftar_tabel if 'absen' in t or 'hadir' in t or 'log' in t]

            cursor_p = db.execute("DESCRIBE guru_pegawai")
            kolom_pegawai = [row[0] for row in cursor_p]

            resp.media = {
                "status": "success",
                "pesan": "Daftar tabel berhasil dikumpulkan, bro!",
                "semua_tabel_di_database": daftar_tabel,
                "tabel_terkait_absensi_atau_log": tabel_terkait,
                "kolom_asli_tabel_guru_pegawai": kolom_pegawai
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal membaca daftar tabel: {str(e)}"
            }