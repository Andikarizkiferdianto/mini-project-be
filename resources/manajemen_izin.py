import falcon
from models.schema import db
from pony.orm import db_session


class ManajemenIzinResource:
    @db_session
    def on_get(self, req, resp):
        id_pegawai = req.get_param('id_pegawai')
        status_filter = req.get_param('status')
        try:
            sql = """
                i.id, p.nama AS nama_pegawai, i.tanggal, i.jenis_izin, i.keterangan, i.status
                FROM log_izin i JOIN guru_pegawai p ON i.id_guru_pegawai = p.id WHERE 1=1
            """
            params = {}
            if id_pegawai:
                sql += " AND i.id_guru_pegawai = $id_pegawai";
                params['id_pegawai'] = int(id_pegawai)
            if status_filter:
                sql += " AND UPPER(i.status) = $status_filter";
                params['status_filter'] = status_filter.strip().upper()
            sql += " ORDER BY i.id DESC"

            raw_data = db.select(sql, params)
            list_izin = [{
                "no": idx, "id": r[0], "nama_pegawai": r[1], "tanggal": str(r[2]),
                "jenis_izin": r[3], "keterangan": r[4], "status": r[5]
            } for idx, r in enumerate(raw_data, start=1)]

            resp.media = {"status": "success", "data": list_izin}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        try:
            raw_data = req.get_media()
            id_guru_pegawai = raw_data.get('id_guru_pegawai')
            tanggal = raw_data.get('tanggal')
            jenis_izin = raw_data.get('jenis_izin')
            keterangan = raw_data.get('keterangan', '')

            if not id_guru_pegawai or not tanggal or not jenis_izin:
                resp.status = falcon.HTTP_400
                resp.media = {"status": "error", "message": "Data nama, tanggal, dan jenis izin wajib diisi!"}
                return

            db.execute("""
                INSERT INTO log_izin (id_guru_pegawai, tanggal, jenis_izin, keterangan, status)
                VALUES ($id_p, $tgl, $jenis, $ket, 'Pending')
            """, {"id_p": int(id_guru_pegawai), "tgl": tanggal, "jenis": jenis_izin, "ket": keterangan})

            resp.media = {"status": "success", "message": "Pengajuan izin berhasil dikirim!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}