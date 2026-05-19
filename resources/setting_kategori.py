import falcon
from models.schema import db
from pony.orm import db_session


class SettingKategoriResource:
    @db_session
    def on_get(self, req, resp):
        """List semua kategori aset"""
        try:
            sql = "SELECT id, nama_kategori FROM setting_kategori_aset ORDER BY id ASC"
            result = db.select(sql)

            data = [{"id": r[0], "nama_kategori": r[1]} for r in result]
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah kategori baru"""
        raw_data = req.get_media()
        try:
            db.execute("INSERT INTO setting_kategori_aset (nama_kategori) VALUES ($nama)",
                       {"nama": raw_data['nama_kategori']})
            resp.media = {"status": "success", "message": "Kategori berhasil ditambahkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus kategori"""
        id_kat = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM setting_kategori_aset WHERE id = $id", {"id": id_kat})
            resp.media = {"status": "success", "message": "Kategori berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}