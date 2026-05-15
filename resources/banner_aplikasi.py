import falcon
from models.schema import db
from pony.orm import db_session


class BannerAplikasiResource:

    # ================= GET =================
    @db_session
    def on_get(self, req, resp):
        try:
            result = db.execute("""
                SELECT id, nama_file, preview_url, diunggah
                FROM banner_aplikasi
                ORDER BY id DESC
            """).fetchall()

            data = [
                {
                    "id": r[0],
                    "nama_file": r[1],
                    "preview": r[2],
                    "diunggah": str(r[3])
                }
                for r in result
            ]

            resp.media = {
                "status": "success",
                "data": data
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    # ================= POST =================
    @db_session
    def on_post(self, req, resp):
        try:
            data = req.get_media()

            db.execute("""
                INSERT INTO banner_aplikasi (nama_file, preview_url)
                VALUES ($file, $url)
            """, {
                "file": data.get("nama_file"),
                "url": data.get("preview_url", "")
            })

            resp.media = {
                "status": "success",
                "message": "Banner berhasil ditambahkan"
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    # ================= DELETE =================
    @db_session
    def on_delete(self, req, resp, banner_id):
        try:
            db.execute("""
                DELETE FROM banner_aplikasi WHERE id = $id
            """, {"id": banner_id})

            resp.media = {
                "status": "success",
                "message": "Banner berhasil dihapus"
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    # ================= OPTIONS (CORS FIX) =================
    def on_options(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_200