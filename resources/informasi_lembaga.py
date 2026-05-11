import falcon
from models.schema import db
from pony.orm import db_session
from datetime import datetime
import traceback


class InformasiLembagaResource:
    @db_session
    def on_get(self, req, resp, info_id=None):
        """Menampilkan List Informasi atau Detail per ID"""
        try:
            if info_id:
                # Ambil satu data berdasarkan ID
                sql = "SELECT id, judul, isi, tanggal FROM informasi_lembaga WHERE id = $id"
                row = db.select(sql, {"id": info_id})

                if not row:
                    resp.status = falcon.HTTP_404
                    resp.media = {"status": "error", "message": "Data tidak ditemukan"}
                    return

                r = row[0]
                data = {
                    "id": r[0],
                    "judul": r[1],
                    "isi": r[2],
                    "tanggal": str(r[3])
                }
            else:
                sql = "SELECT id, judul, isi, tanggal FROM informasi_lembaga ORDER BY id DESC"
                result = db.select(sql)
                data = []
                for r in result:
                    data.append({
                        "id": r[0],
                        "judul": r[1],
                        "isi": r[2],
                        "tanggal": str(r[3])
                    })

            resp.media = {"status": "success", "data": data}

        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah Informasi Baru"""
        raw_data = req.get_media()
        try:
            sql = "INSERT INTO informasi_lembaga (judul, isi, tanggal) VALUES ($judul, $isi, $tgl)"
            db.execute(sql, {
                "judul": raw_data['judul'],
                "isi": raw_data['isi'],
                "tgl": raw_data.get('tanggal', datetime.now().date())
            })
            resp.media = {"status": "success", "message": "Informasi berhasil ditambahkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp, info_id):
        """Edit/Update Informasi berdasarkan ID"""
        raw_data = req.get_media()
        try:
            sql = "UPDATE informasi_lembaga SET judul = $judul, isi = $isi, tanggal = $tgl WHERE id = $id"
            db.execute(sql, {
                "judul": raw_data['judul'],
                "isi": raw_data['isi'],
                "tgl": raw_data['tanggal'],
                "id": info_id
            })
            resp.media = {"status": "success", "message": "Informasi berhasil diperbarui"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, info_id):
        """Hapus Informasi berdasarkan ID"""
        try:
            sql = "DELETE FROM informasi_lembaga WHERE id = $id"
            db.execute(sql, {"id": info_id})
            resp.media = {"status": "success", "message": "Informasi berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}