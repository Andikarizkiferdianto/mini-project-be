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
                    "tanggal": str(r[2]) if r[2] else "",
                    "deskripsi": r[3] if r[3] else ""
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah kegiatan baru ATAU Edit kegiatan lama (Berdasarkan Query Parameter ID)"""
        try:
            id_kegiatan = req.get_param_as_int('id')
            raw_data = req.get_media()

            judul = raw_data.get('judul')
            tanggal = raw_data.get('tanggal')
            deskripsi = raw_data.get('deskripsi') or ""

            if not judul or not tanggal:
                raise ValueError("Judul dan Tanggal kegiatan wajib diisi!")

            # Skenario Edit Data (Jika parameter id tersedia)
            if id_kegiatan:
                sql = """
                    UPDATE kegiatan_sekolah 
                    SET judul = $judul, tanggal = $tanggal, deskripsi = $deskripsi 
                    WHERE id = $id
                """
                db.execute(sql, {
                    "id": id_kegiatan,
                    "judul": judul,
                    "tanggal": tanggal,
                    "deskripsi": deskripsi
                })
                resp.media = {"status": "success", "message": "Kegiatan sekolah berhasil diperbarui!"}

            # Skenario Tambah Data Baru
            else:
                sql = """
                    INSERT INTO kegiatan_sekolah (judul, tanggal, deskripsi)
                    VALUES ($judul, $tanggal, $deskripsi)
                """
                db.execute(sql, {
                    "judul": judul,
                    "tanggal": tanggal,
                    "deskripsi": deskripsi
                })
                resp.media = {"status": "success", "message": "Kegiatan sekolah berhasil ditambahkan!"}

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus kegiatan berdasarkan ID (?id=...)"""
        try:
            id_kegiatan = req.get_param_as_int('id')
            if not id_kegiatan:
                raise ValueError("Parameter ID tidak ditemukan.")

            db.execute("DELETE FROM kegiatan_sekolah WHERE id = $id", {"id": id_kegiatan})
            resp.media = {"status": "success", "message": "Kegiatan berhasil dihapus dari sistem!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}