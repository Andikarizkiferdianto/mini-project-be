import falcon
from models.schema import db
from pony.orm import db_session

class KelolaIndikatorResource:
    @db_session
    def on_get(self, req, resp, id_indikator=None):
        """Ambil semua indikator atau detail 1 indikator berdasarkan ID"""
        try:
            if id_indikator:
                sql = "SELECT id, nama_indikator, bobot, keterangan FROM setting_indikator WHERE id = $id"
                result = db.select(sql, {"id": int(id_indikator)})
                if not result:
                    resp.status = falcon.HTTP_404
                    resp.media = {"status": "error", "message": "Indikator tidak ditemukan"}
                    return
                r = result[0]
                resp.media = {
                    "status": "success",
                    "data": {"id": r[0], "nama_indikator": r[1], "bobot": r[2], "keterangan": r[3]}
                }
                return

            sql = "SELECT id, nama_indikator, bobot, keterangan FROM setting_indikator ORDER BY id ASC"
            result = db.select(sql)
            data = []
            for r in result:
                data.append({
                    "id": r[0],
                    "nama_indikator": r[1],
                    "bobot": r[2],
                    "keterangan": r[3]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp, id_indikator=None):
        """Tambah indikator penilaian baru"""
        try:
            raw_data = req.get_media()
            sql = """
                INSERT INTO setting_indikator (nama_indikator, bobot, keterangan)
                VALUES ($nama, $bobot, $keterangan)
            """
            db.execute(sql, {
                "nama": raw_data.get('nama_indikator'),
                "bobot": int(raw_data.get('bobot')),
                "keterangan": raw_data.get('keterangan', '-')
            })
            resp.media = {"status": "success", "message": "Indikator penilaian berhasil ditambahkan!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp, id_indikator=None):
        """Edit / Update data indikator berdasarkan ID di URL"""
        if not id_indikator:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "ID Indikator harus dikirim di URL"}
            return
        try:
            raw_data = req.get_media()
            sql = """
                UPDATE setting_indikator 
                SET nama_indikator = $nama, bobot = $bobot, keterangan = $keterangan 
                WHERE id = $id
            """
            db.execute(sql, {
                "id": int(id_indikator),
                "nama": raw_data.get('nama_indikator'),
                "bobot": int(raw_data.get('bobot')),
                "keterangan": raw_data.get('keterangan')
            })
            resp.media = {"status": "success", "message": "Indikator penilaian berhasil diperbarui!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id_indikator=None):
        """Hapus indikator berdasarkan ID di URL"""
        if not id_indikator:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "ID Indikator harus dikirim di URL"}
            return
        try:
            db.execute("DELETE FROM setting_indikator WHERE id = $id", {"id": int(id_indikator)})
            resp.media = {"status": "success", "message": "Indikator berhasil dihapus!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}