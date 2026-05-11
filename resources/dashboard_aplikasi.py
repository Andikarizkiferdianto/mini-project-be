import falcon
from models.schema import db
from pony.orm import db_session

class DashboardAplikasiResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil statistik ringkasan untuk dashboard"""
        try:
            # 1. Hitung Total User (Siswa + Guru)
            total_siswa = db.select("SELECT COUNT(*) FROM siswa")[0]
            total_guru = db.select("SELECT COUNT(*) FROM guru")[0]
            total_users = total_siswa + total_guru

            total_banner = db.select("SELECT COUNT(*) FROM banner_aplikasi")[0]

            total_info = db.select("SELECT COUNT(*) FROM informasi_lembaga")[0]

            total_backup = db.select("SELECT COUNT(*) FROM riwayat_backup")[0]

            resp.media = {
                "status": "success",
                "data": {
                    "total_users": total_users,
                    "total_banner": total_banner,
                    "total_informasi": total_info,
                    "total_backup": total_backup
                }
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}