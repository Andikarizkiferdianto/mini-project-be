import falcon
from models.schema import db
from pony.orm import db_session


class ManajemenCutiResource:

    @db_session
    def on_get(self, req, resp, id_cuti=None):

        try:

            id_pegawai = req.get_param('id_pegawai')
            status = req.get_param('status')

            sql = """
                SELECT
                    lc.id,
                    gp.nama,
                    lc.tanggal_mulai,
                    lc.tanggal_selesai,
                    lc.alasan,
                    lc.status,
                    lc.id_guru_pegawai
                FROM log_cuti lc
                LEFT JOIN guru_pegawai gp
                    ON lc.id_guru_pegawai = gp.id
            """

            kondisi = []

            if id_pegawai:
                kondisi.append(f"lc.id_guru_pegawai = {int(id_pegawai)}")

            if status:
                kondisi.append(f"lc.status = '{status}'")

            if kondisi:
                sql += " WHERE " + " AND ".join(kondisi)

            sql += " ORDER BY lc.id DESC"

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute(sql)

            raw_data = cursor.fetchall()

            data = []

            for r in raw_data:
                data.append({
                    "id": r[0],
                    "nama_pegawai": r[1],
                    "tanggal_mulai": str(r[2]),
                    "tanggal_selesai": str(r[3]),
                    "alasan": r[4],
                    "status": r[5],
                    "id_guru_pegawai": r[6]
                })

            resp.media = {
                "status": "success",
                "data": data
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_post(self, req, resp):

        try:

            data = req.get_media()

            sql = """
                INSERT INTO log_cuti
                (
                    id_guru_pegawai,
                    tanggal_mulai,
                    tanggal_selesai,
                    alasan,
                    status
                )
                VALUES
                (
                    $id_guru_pegawai,
                    $tanggal_mulai,
                    $tanggal_selesai,
                    $alasan,
                    'Pending'
                )
            """

            db.execute(sql, {
                "id_guru_pegawai": int(data['id_guru_pegawai']),
                "tanggal_mulai": data['tanggal_mulai'],
                "tanggal_selesai": data['tanggal_selesai'],
                "alasan": data.get('alasan', '')
            })

            resp.media = {
                "status": "success",
                "message": "Data cuti berhasil ditambahkan"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_put(self, req, resp, id_cuti):

        try:

            data = req.get_media()

            sql = """
                UPDATE log_cuti
                SET
                    id_guru_pegawai = $id_guru_pegawai,
                    tanggal_mulai = $tanggal_mulai,
                    tanggal_selesai = $tanggal_selesai,
                    alasan = $alasan
                WHERE id = $id
            """

            db.execute(sql, {
                "id": int(id_cuti),
                "id_guru_pegawai": int(data['id_guru_pegawai']),
                "tanggal_mulai": data['tanggal_mulai'],
                "tanggal_selesai": data['tanggal_selesai'],
                "alasan": data.get('alasan', '')
            })

            resp.media = {
                "status": "success",
                "message": "Data berhasil diupdate"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, id_cuti):

        try:

            db.execute(
                "DELETE FROM log_cuti WHERE id = $id",
                {"id": int(id_cuti)}
            )

            resp.media = {
                "status": "success",
                "message": "Data berhasil dihapus"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }