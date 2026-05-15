import falcon
from models.schema import db
from pony.orm import db_session
import traceback


class SettingUserResource:

    @db_session
    def on_get(self, req, resp):
        try:
            # FIX: pakai execute (bukan select string)
            kelas = db.execute("SELECT id, nama_kelas FROM kelas")

            resp.media = {
                "status": "success",
                "options": {
                    "kelas": [{"id": k[0], "nama": k[1]} for k in kelas],
                    "jenis_user": ["Siswa", "Guru", "Wali Kelas", "Orang Tua"]
                }
            }

        except Exception as e:
            print("ERROR ON_GET:", traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "options": {  # penting: biar frontend tidak crash
                    "kelas": [],
                    "jenis_user": []
                },
                "message": str(e)
            }

    @db_session
    def on_post(self, req, resp):
        try:
            raw = req.get_media()
            jenis = raw.get("jenis_user")
            kelas_id = raw.get("kelas_id")

            data = []

            if jenis == "Siswa":

                if kelas_id:
                    siswa_list = db.execute("""
                        SELECT id, nisn, nama
                        FROM siswa
                        WHERE id_kelas = $id_kelas
                    """, {"id_kelas": kelas_id})
                else:
                    siswa_list = db.execute("SELECT id, nisn, nama FROM siswa")

                for s in siswa_list:
                    data.append({
                        "id": s[0],
                        "nis_id": s[1],
                        "nama": s[2],
                        "username": s[1],
                        "password": ""
                    })

            else:
                guru_list = db.execute("SELECT id, nip, nama FROM guru")

                for g in guru_list:
                    data.append({
                        "id": g[0],
                        "nis_id": g[1],
                        "nama": g[2],
                        "username": g[1],
                        "password": ""
                    })

            resp.media = {"status": "success", "data": data}

        except Exception as e:
            print("ERROR ON_POST:", traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "data": []}
