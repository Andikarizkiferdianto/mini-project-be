import falcon
from models.schema import db
from pony.orm import db_session


class DataGuruDanKaryawanResource:
    @db_session
    def on_get(self, req, resp, id_pegawai=None):
        """Ambil list data guru/karyawan, atau ambil detail 1 orang jika ID dikirim"""
        try:
            if id_pegawai:
                sql = "SELECT id, tipe, nama, nip, jabatan, no_hp, email, status FROM guru_pegawai WHERE id = $id"
                result = db.select(sql, {"id": int(id_pegawai)})
                if not result:
                    resp.status = falcon.HTTP_404
                    resp.media = {"status": "error", "message": "Data tidak ditemukan"}
                    return
                r = result[0]
                resp.media = {
                    "status": "success",
                    "data": {
                        "id": r[0], "tipe": r[1], "nama": r[2], "nip": r[3],
                        "jabatan": r[4], "no_hp": r[5], "email": r[6], "status": r[7]
                    }
                }
                return

            # Ambil parameter tipe query string (?tipe=GURU atau ?tipe=PEGAWAI)
            tipe = req.get_param('tipe')
            if tipe:
                sql = "SELECT id, tipe, nama, nip, jabatan, no_hp, email, status FROM guru_pegawai WHERE LOWER(tipe) = LOWER($tipe) ORDER BY id DESC"
                result = db.select(sql, {"tipe": tipe})
            else:
                sql = "SELECT id, tipe, nama, nip, jabatan, no_hp, email, status FROM guru_pegawai ORDER BY id DESC"
                result = db.select(sql)

            data = []
            for r in result:
                data.append({
                    "id": r[0], "tipe": r[1], "nama": r[2], "nip": r[3],
                    "jabatan": r[4], "no_hp": r[5], "email": r[6], "status": r[7]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp, id_pegawai=None):
        """Tambah data Guru / Karyawan baru"""
        try:
            raw_data = req.get_media()
            sql = """
                INSERT INTO guru_pegawai (tipe, nama, nip, jabatan, no_hp, email, status)
                VALUES ($tipe, $nama, $nip, $jabatan, $no_hp, $email, $status)
            """
            db.execute(sql, {
                "tipe": raw_data.get('tipe', 'GURU').upper(),
                "nama": raw_data.get('nama'),
                "nip": raw_data.get('nip', '-'),
                "jabatan": raw_data.get('jabatan'),
                "no_hp": raw_data.get('no_hp', '-'),
                "email": raw_data.get('email', '-'),
                "status": raw_data.get('status', 'Aktif')
            })
            resp.media = {"status": "success", "message": "Data berhasil ditambahkan!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp, id_pegawai=None):
        """Edit / Update data Guru atau Karyawan berdasarkan ID di URL"""
        if not id_pegawai:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "ID Pegawai harus dikirim di URL"}
            return

        try:
            raw_data = req.get_media()
            sql = """
                UPDATE guru_pegawai 
                SET tipe = $tipe, nama = $nama, nip = $nip, jabatan = $jabatan, 
                    no_hp = $no_hp, email = $email, status = $status 
                WHERE id = $id
            """
            db.execute(sql, {
                "id": int(id_pegawai),
                "tipe": raw_data.get('tipe').upper(),
                "nama": raw_data.get('nama'),
                "nip": raw_data.get('nip'),
                "jabatan": raw_data.get('jabatan'),
                "no_hp": raw_data.get('no_hp'),
                "email": raw_data.get('email'),
                "status": raw_data.get('status')
            })
            resp.media = {"status": "success", "message": "Data berhasil diperbarui!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id_pegawai=None):
        """Hapus data kepegawaian berdasarkan ID di URL"""
        if not id_pegawai:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "ID Pegawai harus dikirim di URL"}
            return

        try:
            db.execute("DELETE FROM guru_pegawai WHERE id = $id", {"id": int(id_pegawai)})
            resp.media = {"status": "success", "message": "Data berhasil dihapus!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}