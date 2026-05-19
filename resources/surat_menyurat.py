import falcon
import os
import uuid
from models.schema import db
from pony.orm import db_session

class SuratMenyuratResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil daftar semua surat"""
        try:
            sql = "SELECT * FROM arsip_surat ORDER BY id DESC"
            result = db.select(sql)
            data = []
            for r in result:
                data.append({
                    "id": r[0], "nomor_surat": r[1],
                    "tgl_surat": str(r[2]), "tgl_terima": str(r[3]),
                    "sumber_surat": r[4], "perihal": r[5],
                    "jenis_surat": r[6], "file_surat": r[7],
                    "keterangan": r[8]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah Surat & Upload File Scan"""
        try:
            form = req.get_media()
            fields = {}
            nama_file_baru = None

            for part in form:
                if part.name == 'file_surat' and part.filename:
                    ext = os.path.splitext(part.filename)[1]
                    nama_file_baru = f"surat_{uuid.uuid4().hex}{ext}"
                    path_simpan = os.path.join('uploads', 'surat', nama_file_baru)
                    with open(path_simpan, 'wb') as f:
                        f.write(part.data)
                else:
                    fields[part.name] = part.text

            sql = """
                INSERT INTO arsip_surat (nomor_surat, tgl_surat, tgl_terima, sumber_surat, perihal, jenis_surat, file_surat, keterangan)
                VALUES ($no, $tgl_s, $tgl_t, $sumber, $perihal, $jenis, $file, $ket)
            """
            db.execute(sql, {
                "no": fields.get('nomor_surat'), "tgl_s": fields.get('tgl_surat'),
                "tgl_t": fields.get('tgl_terima'), "sumber": fields.get('sumber_surat'),
                "perihal": fields.get('perihal'), "jenis": fields.get('jenis_surat', 'Masuk'),
                "file": nama_file_baru, "ket": fields.get('keterangan')
            })
            resp.media = {"status": "success", "message": "Surat berhasil diarsipkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus arsip surat"""
        id_surat = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM arsip_surat WHERE id = $id", {"id": id_surat})
            resp.media = {"status": "success", "message": "Arsip surat berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}