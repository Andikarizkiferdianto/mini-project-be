import falcon
from models.schema import db
from pony.orm import db_session


class ManajemenLemburResource:
    @db_session
    def on_get(self, req, resp):
        id_pegawai = req.get_param('id_pegawai')
        status_filter = req.get_param('status')
        try:
            sql = """
                l.id, p.nama AS nama_pegawai, l.tanggal, l.jam_mulai, l.jam_selesai, l.kegiatan, l.status
                FROM log_lembur l JOIN guru_pegawai p ON l.id_guru_pegawai = p.id WHERE 1=1
            """
            params = {}
            if id_pegawai:
                sql += " AND l.id_guru_pegawai = $id_pegawai";
                params['id_pegawai'] = int(id_pegawai)
            if status_filter:
                sql += " AND UPPER(l.status) = $status_filter";
                params['status_filter'] = status_filter.strip().upper()
            sql += " ORDER BY l.id DESC"

            raw_data = db.select(sql, params)
            list_lembur = [{
                "no": idx, "id": r[0], "nama_pegawai": r[1], "tanggal": str(r[2]),
                "jam_mulai": str(r[3]), "jam_selesai": str(r[4]), "kegiatan": r[5], "status": r[6]
            } for idx, r in enumerate(raw_data, start=1)]

            resp.media = {"status": "success", "data": list_lembur}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        try:
            raw_data = req.get_media()
            id_guru_pegawai = raw_data.get('id_guru_pegawai')
            tanggal = raw_data.get('tanggal')
            jam_mulai = raw_data.get('jam_mulai')
            jam_selesai = raw_data.get('jam_selesai')
            kegiatan = raw_data.get('kegiatan', '')

            if not id_guru_pegawai or not tanggal or not jam_mulai or not jam_selesai:
                resp.status = falcon.HTTP_400
                resp.media = {"status": "error", "message": "Data pengajuan lembur tidak lengkap!"}
                return

            db.execute("""
                INSERT INTO log_lembur (id_guru_pegawai, tanggal, jam_mulai, jam_selesai, kegiatan, status)
                VALUES ($id_p, $tgl, $mulai, $selesai, $keg, 'Pending')
            """, {"id_p": int(id_guru_pegawai), "tgl": tanggal, "mulai": jam_mulai, "selesai": jam_selesai,
                  "keg": kegiatan})

            resp.media = {"status": "success", "message": "Pengajuan lembur berhasil dikirim!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}