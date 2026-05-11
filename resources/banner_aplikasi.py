import falcon
from models.schema import db
from pony.orm import db_session
import traceback

class BannerAplikasiResource:
    @db_session
    def on_get(self, req, resp):
        """Menampilkan daftar banner untuk tabel UI"""
        try:
            sql = "SELECT id, nama_file, preview_url, diunggah FROM banner_aplikasi ORDER BY id DESC"
            result = db.select(sql)
            data = []
            for r in result:
                data.append({
                    "id": r[0],
                    "nama_file": r[1],
                    "preview": r[2],
                    "diunggah": str(r[3])
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah Banner (Simpan info file)"""
        raw_data = req.get_media()
        try:
            sql = "INSERT INTO banner_aplikasi (nama_file, preview_url) VALUES ($file, $url)"
            db.execute(sql, {
                "file": raw_data['nama_file'],
                "url": raw_data.get('preview_url', '')
            })
            resp.media = {"status": "success", "message": "Banner berhasil ditambahkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, banner_id):
        """Hapus Banner berdasarkan ID"""
        try:
            db.execute("DELETE FROM banner_aplikasi WHERE id = $id", {"id": banner_id})
            resp.media = {"status": "success", "message": "Banner berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}