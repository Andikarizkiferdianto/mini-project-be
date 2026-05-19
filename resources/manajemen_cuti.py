import falcon
from models.schema import db
from pony.orm import db_session


class ManajemenCutiResource:
    @db_session
    def on_get(self, req, resp):
        """Mengambil data pengajuan cuti, izin, atau lembur dengan filter dinamis"""
        id_pegawai = req.get_param('id_pegawai')
        status_filter = req.get_param('status')

        try:
            sql = """
                c.id,
                p.nama AS nama_pegawai,
                c.tanggal_mulai,
                c.tanggal_selesai,
                c.alasan,
                c.status
                FROM log_cuti c
                JOIN guru_pegawai p ON c.id_guru_pegawai = p.id
                WHERE 1=1
            """
            params = {}

            if id_pegawai:
                sql += " AND c.id_guru_pegawai = $id_pegawai"
                params['id_pegawai'] = int(id_pegawai)

            if status_filter:
                sql += " AND UPPER(c.status) = $status_filter"
                params['status_filter'] = status_filter.strip().upper()

            sql += " ORDER BY c.id DESC"

            raw_data = db.select(sql, params)

            list_cuti = []
            for idx, row in enumerate(raw_data, start=1):
                list_cuti.append({
                    "no": idx,
                    "id": row[0],
                    "nama_pegawai": row[1],
                    "tanggal_mulai": str(row[2]),
                    "tanggal_selesai": str(row[3]),
                    "alasan": row[4],
                    "status": row[5]
                })

            resp.media = {
                "status": "success",
                "data": list_cuti
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Gagal mengambil data cuti: {str(e)}"}

    @db_session
    def on_post(self, req, resp):
        """Menyimpan pengajuan cuti baru dari form modal"""
        try:
            raw_data = req.get_media()

            id_guru_pegawai = raw_data.get('id_guru_pegawai')
            tanggal_mulai = raw_data.get('tanggal_mulai')
            tanggal_selesai = raw_data.get('tanggal_selesai')
            alasan = raw_data.get('alasan', '')

            if not id_guru_pegawai or not tanggal_mulai or not tanggal_selesai:
                resp.status = falcon.HTTP_400
                resp.media = {"status": "error",
                              "message": "Data nama pegawai, tanggal mulai, dan tanggal selesai wajib diisi!"}
                return

            sql_insert = """
                INSERT INTO log_cuti (id_guru_pegawai, tanggal_mulai, tanggal_selesai, alasan, status)
                VALUES ($id_pegawai, $tgl_mulai, $tgl_selesai, $alasan, 'Pending')
            """

            db.execute(sql_insert, {
                "id_pegawai": int(id_guru_pegawai),
                "tgl_mulai": tanggal_mulai,
                "tgl_selesai": tanggal_selesai,
                "alasan": alasan
            })

            resp.media = {
                "status": "success",
                "message": "Pengajuan cuti/izin berhasil dikirim!"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Gagal memproses pengajuan cuti: {str(e)}"}