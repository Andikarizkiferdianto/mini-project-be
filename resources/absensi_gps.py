import falcon
from models.schema import db
from pony.orm import db_session


class AbsensiGpsResource:
    @db_session
    def on_get(self, req, resp):
        """Menampilkan semua list lokasi absensi"""
        try:
            sql = "SELECT id, nama_lokasi, latitude, longitude, radius, jam_masuk, jam_selesai FROM setting_absensi_gps"
            result = db.select(sql)

            data = []
            for r in result:
                data.append({
                    "id": r[0],
                    "nama_lokasi": r[1],
                    "latitude": float(r[2]),
                    "longitude": float(r[3]),
                    "radius": r[4],
                    "jam_masuk": str(r[5]),
                    "jam_selesai": str(r[6])
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Simpan lokasi baru"""
        raw_data = req.get_media()
        try:
            sql = """
                INSERT INTO setting_absensi_gps (nama_lokasi, latitude, longitude, radius, jam_masuk, jam_selesai)
                VALUES ($nama, $lat, $lng, $rad, $masuk, $selesai)
            """
            db.execute(sql, {
                "nama": raw_data['nama_lokasi'],
                "lat": raw_data['latitude'],
                "lng": raw_data['longitude'],
                "rad": raw_data['radius'],
                "masuk": raw_data['jam_masuk'],
                "selesai": raw_data['jam_selesai']
            })
            resp.media = {"status": "success", "message": "Lokasi absensi berhasil ditambahkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp):
        """Update lokasi yang sudah ada"""
        raw_data = req.get_media()
        try:
            sql = """
                UPDATE setting_absensi_gps 
                SET nama_lokasi=$nama, latitude=$lat, longitude=$lng, radius=$rad, jam_masuk=$masuk, jam_selesai=$selesai
                WHERE id=$id
            """
            db.execute(sql, {
                "id": raw_data['id'],
                "nama": raw_data['nama_lokasi'],
                "lat": raw_data['latitude'],
                "lng": raw_data['longitude'],
                "rad": raw_data['radius'],
                "masuk": raw_data['jam_masuk'],
                "selesai": raw_data['jam_selesai']
            })
            resp.media = {"status": "success", "message": "Data lokasi berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus lokasi"""
        # Cara ambil ID dari parameter URL: /api/absensi-gps?id=1
        id_lokasi = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM setting_absensi_gps WHERE id = $id", {"id": id_lokasi})
            resp.media = {"status": "success", "message": "Lokasi berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}