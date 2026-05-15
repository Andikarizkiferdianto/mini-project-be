import falcon
from models.schema import db
from pony.orm import db_session

class DashboardAplikasiResource:

    @db_session
    def on_get(self, req, resp):

        try:
            conn = db.get_connection()
            cursor = conn.cursor()

            # helper aman
            def count_table(table):
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    return cursor.fetchone()[0]
                except:
                    return 0

            # USERS
            cursor.execute("SELECT COUNT(*) FROM siswa")
            total_siswa = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM guru")
            total_guru = cursor.fetchone()[0]

            total_users = total_siswa + total_guru

            # DASHBOARD ITEMS (AMAN)
            total_banner = count_table("banner_aplikasi")
            total_info = count_table("informasi_lembaga")
            total_backup = count_table("riwayat_backup")

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
            resp.media = {
                "status": "error",
                "message": str(e)
            }