import falcon
from models.schema import db
from pony.orm import db_session


class KegiatanSekolahResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil semua daftar kegiatan sekolah"""
        try:
            sql = "SELECT id, judul, tanggal, deskripsi FROM kegiatan_sekolah ORDER BY tanggal DESC"
            result = db.select(sql)

            data = []
            for r in result:
                data.append({
                    "id": r[0],
                    "judul": r[1],
                    "tanggal": str(r[2]),
                    "deskripsi": r[3]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah kegiatan baru"""
        try:
            raw_data = req.get_media()

            sql = """
                INSERT INTO kegiatan_sekolah (judul, tanggal, deskripsi)
                VALUES ($judul, $tanggal, $deskripsi)
            """
            db.execute(sql, {
                "judul": raw_data.get('judul'),
                "tanggal": raw_data.get('tanggal'),
                "deskripsi": raw_data.get('deskripsi')
            })
            resp.media = {"status": "success", "message": "Kegiatan sekolah berhasil ditambahkan!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp):
        """Edit / Update kegiatan sekolah"""
        try:
            raw_data = req.get_media()

            sql = """
                UPDATE kegiatan_sekolah 
                SET judul = $judul, tanggal = $tanggal, deskripsi = $deskripsi 
                WHERE id = $id
            """
            db.execute(sql, {
                "id": raw_data.get('id'),
                "judul": raw_data.get('judul'),
                "tanggal": raw_data.get('tanggal'),
                "deskripsi": raw_data.get('deskripsi')
            })
            resp.media = {"status": "success", "message": "Kegiatan sekolah berhasil diperbarui!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus kegiatan berdasarkan ID"""
        id_kegiatan = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM kegiatan_sekolah WHERE id = $id", {"id": id_kegiatan})
            resp.media = {"status": "success", "message": "Kegiatan berhasil dihapus!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}