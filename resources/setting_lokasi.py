import falcon
from models.schema import db
from pony.orm import db_session


class SettingLokasiResource:
    @db_session
    def on_get(self, req, resp):
        """List semua lokasi aset"""
        try:
            sql = "SELECT id, nama_lokasi FROM setting_lokasi_aset ORDER BY id ASC"
            result = db.select(sql)

            data = [{"id": r[0], "nama_lokasi": r[1]} for r in result]
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah lokasi baru"""
        raw_data = req.get_media()
        try:
            db.execute("INSERT INTO setting_lokasi_aset (nama_lokasi) VALUES ($nama)",
                       {"nama": raw_data['nama_lokasi']})
            resp.media = {"status": "success", "message": "Lokasi berhasil ditambahkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus lokasi"""
        id_lokasi = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM setting_lokasi_aset WHERE id = $id", {"id": id_lokasi})
            resp.media = {"status": "success", "message": "Lokasi berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}