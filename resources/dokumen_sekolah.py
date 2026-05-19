import falcon
import os
import uuid
from models.schema import db
from pony.orm import db_session


class DokumenSekolahResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil list semua dokumen sekolah"""
        try:
            sql = "SELECT id, judul, tanggal, deskripsi, file_dokumen FROM dokumen_sekolah ORDER BY id DESC"
            result = db.select(sql)

            data = []
            for r in result:
                data.append({
                    "id": r[0],
                    "judul": r[1],
                    "tanggal": str(r[2]),
                    "deskripsi": r[3],
                    "file_dokumen": r[4]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah data dokumen baru beserta upload file"""
        try:
            form = req.get_media()
            fields = {'judul': '', 'tanggal': '', 'deskripsi': ''}
            nama_file_baru = None

            for part in form:
                if part.name == 'file_dokumen' and part.filename:
                    ext = os.path.splitext(part.filename)[1]
                    nama_file_baru = f"dok_{uuid.uuid4().hex}{ext}"
                    path_simpan = os.path.join('uploads', 'dokumen', nama_file_baru)

                    os.makedirs(os.path.dirname(path_simpan), exist_ok=True)

                    with open(path_simpan, 'wb') as f:
                        f.write(part.data)
                else:
                    if part.name in fields:
                        fields[part.name] = part.text

            sql = """
                INSERT INTO dokumen_sekolah (judul, tanggal, deskripsi, file_dokumen)
                VALUES ($judul, $tanggal, $deskripsi, $file)
            """
            db.execute(sql, {
                "judul": fields['judul'],
                "tanggal": fields['tanggal'],
                "deskripsi": fields['deskripsi'],
                "file": nama_file_baru
            })
            resp.media = {"status": "success", "message": "Dokumen sekolah berhasil disimpan!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus dokumen berdasarkan ID"""
        id_dok = req.get_param_as_int('id')
        try:
            res = db.select("SELECT file_dokumen FROM dokumen_sekolah WHERE id = $id", {"id": id_dok})
            if res and res[0]:
                path_file = os.path.join('uploads', 'dokumen', res[0])
                if os.path.exists(path_file):
                    os.remove(path_file)

            db.execute("DELETE FROM dokumen_sekolah WHERE id = $id", {"id": id_dok})
            resp.media = {"status": "success", "message": "Dokumen berhasil dihapus!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}