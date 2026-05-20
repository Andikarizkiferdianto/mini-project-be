import falcon
from models.schema import db
from pony.orm import db_session


class AbsensiGpsResource:

    @db_session
    def on_get(self, req, resp):

        try:

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    nama_lokasi,
                    latitude,
                    longitude,
                    radius,
                    jam_masuk,
                    jam_selesai
                FROM setting_lokasi_aset
                ORDER BY id ASC
            """)

            result = cursor.fetchall()

            data = []

            for row in result:

                data.append({
                    "id": row[0],
                    "nama_lokasi": row[1],
                    "latitude": row[2],
                    "longitude": row[3],
                    "radius": row[4],
                    "jam_masuk": str(row[5]),
                    "jam_selesai": str(row[6]),
                })

            resp.media = {
                "status": "success",
                "data": data
            }

        except Exception as e:

            print("ERROR GET:", e)

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_post(self, req, resp):

        data = req.get_media()

        try:

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO setting_lokasi_aset
                (
                    nama_lokasi,
                    latitude,
                    longitude,
                    radius,
                    jam_masuk,
                    jam_selesai
                )
                VALUES
                (%s, %s, %s, %s, %s, %s)
            """, (
                data["nama_lokasi"],
                data["latitude"],
                data["longitude"],
                data["radius"],
                data["jam_masuk"],
                data["jam_selesai"]
            ))

            conn.commit()

            resp.media = {
                "status": "success",
                "message": "Lokasi berhasil ditambahkan"
            }

        except Exception as e:

            print("ERROR POST:", e)

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp):

        id_lokasi = req.get_param_as_int("id")

        try:

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM setting_lokasi_aset
                WHERE id = %s
            """, (id_lokasi,))

            conn.commit()

            resp.media = {
                "status": "success",
                "message": "Lokasi berhasil dihapus"
            }

        except Exception as e:

            print("ERROR DELETE:", e)

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }