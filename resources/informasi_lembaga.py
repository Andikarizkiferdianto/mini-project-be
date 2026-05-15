import falcon
from pony.orm import db_session
from models.schema import db
from datetime import datetime
import traceback


class InformasiLembagaResource:

    @db_session
    def on_get(self, req, resp, info_id=None):

        try:

            conn = db.get_connection()
            cursor = conn.cursor()

            if info_id:

                cursor.execute("""
                    SELECT id, judul, isi, tanggal
                    FROM informasi_lembaga
                    WHERE id=%s
                """, [info_id])

                row = cursor.fetchone()

                if not row:
                    resp.media = {
                        "status": "error",
                        "message": "Data tidak ditemukan"
                    }
                    return

                data = {
                    "id": row[0],
                    "judul": row[1],
                    "isi": row[2],
                    "tanggal": str(row[3])
                }

            else:

                cursor.execute("""
                    SELECT id, judul, isi, tanggal
                    FROM informasi_lembaga
                    ORDER BY id DESC
                """)

                rows = cursor.fetchall()

                data = []

                for row in rows:
                    data.append({
                        "id": row[0],
                        "judul": row[1],
                        "isi": row[2],
                        "tanggal": str(row[3])
                    })

            resp.media = {
                "status": "success",
                "data": data
            }

        except Exception as e:

            print(traceback.format_exc())

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_post(self, req, resp):

        try:

            raw_data = req.get_media()

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO informasi_lembaga
                (judul, isi, tanggal)
                VALUES (%s, %s, %s)
            """, (
                raw_data['judul'],
                raw_data['isi'],
                raw_data['tanggal']
            ))

            conn.commit()

            resp.media = {
                "status": "success",
                "message": "Informasi berhasil ditambahkan"
            }

        except Exception as e:

            print(traceback.format_exc())

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_put(self, req, resp, info_id):

        try:

            raw_data = req.get_media()

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE informasi_lembaga
                SET judul=%s,
                    isi=%s,
                    tanggal=%s
                WHERE id=%s
            """, (
                raw_data['judul'],
                raw_data['isi'],
                raw_data['tanggal'],
                info_id
            ))

            conn.commit()

            resp.media = {
                "status": "success",
                "message": "Informasi berhasil diupdate"
            }

        except Exception as e:

            print(traceback.format_exc())

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, info_id):

        try:

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM informasi_lembaga WHERE id=%s",
                [info_id]
            )

            conn.commit()

            resp.media = {
                "status": "success",
                "message": "Informasi berhasil dihapus"
            }

        except Exception as e:

            print(traceback.format_exc())

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }