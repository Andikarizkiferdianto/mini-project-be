import falcon
from models.schema import db
from pony.orm import db_session


class SettingLokasiResource:

    @db_session
    def on_get(self, req, resp):
        """Membaca semua daftar lokasi inventaris aset (Tabel Terpisah)"""
        try:
            # Gunakan tabel baru khusus inventaris
            sql = "SELECT id, nama_lokasi FROM setting_lokasi_inventaris ORDER BY id ASC"
            cursor = db.execute(sql)
            result = cursor.fetchall()

            data = [{"id": r[0], "nama_lokasi": r[1]} for r in result]
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Menambahkan lokasi inventaris baru"""
        raw_data = req.get_media()
        try:
            db.execute(
                "INSERT INTO setting_lokasi_inventaris (nama_lokasi) VALUES ($nama)",
                {"nama": raw_data["nama_lokasi"]},
            )
            resp.media = {
                "status": "success",
                "message": "Lokasi aset berhasil ditambahkan",
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp):
        """Memperbarui nama lokasi inventaris"""
        raw_data = req.get_media()
        try:
            db.execute(
                "UPDATE setting_lokasi_inventaris SET nama_lokasi=$nama WHERE id=$id",
                {"id": int(raw_data["id"]), "nama": raw_data["nama_lokasi"]},
            )
            resp.media = {
                "status": "success",
                "message": "Lokasi aset berhasil diperbarui",
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Menghapus lokasi inventaris"""
        id_lokasi = req.get_param_as_int("id")
        try:
            db.execute(
                "DELETE FROM setting_lokasi_inventaris WHERE id = $id",
                {"id": id_lokasi},
            )
            resp.media = {
                "status": "success",
                "message": "Lokasi aset berhasil dihapus",
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}