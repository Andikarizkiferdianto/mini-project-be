import falcon
from models.schema import db
from pony.orm import db_session
from datetime import datetime

class RiwayatAsetResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil semua riwayat aktivitas aset dengan join aman"""
        try:
            sql = """
                SELECT r.id, a.nama_aset, r.aktivitas, r.keterangan, r.pengguna, r.tanggal, r.id_aset 
                FROM riwayat_aset r 
                JOIN inventaris_aset a ON r.id_aset = a.id 
                ORDER BY r.tanggal DESC
            """
            cursor = db.execute(sql)
            result = cursor.fetchall()

            data = []
            for r in result:
                tgl_obj = r[5]
                # Format objek datetime dari MySQL ke string siap cetak
                if isinstance(tgl_obj, datetime):
                    tanggal_str = tgl_obj.strftime('%d %b %Y %H:%M')
                else:
                    tanggal_str = str(tgl_obj) if tgl_obj else "-"

                data.append({
                    "id": r[0],
                    "nama_aset": r[1],
                    "aktivitas": r[2],
                    "keterangan": r[3],
                    "pengguna": r[4],
                    "tanggal": tanggal_str,
                    "id_aset": r[6]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah Catatan Aktivitas Baru + Otomatis Tanggal Berfungsi"""
        raw_data = req.get_media()
        try:
            # Menggunakan fungsi NOW() MySQL agar tanggal otomatis terisi waktu saat ini
            sql = """
                INSERT INTO riwayat_aset (id_aset, aktivitas, keterangan, pengguna, tanggal)
                VALUES ($id_aset, $aktivitas, $ket, $user, NOW())
            """
            db.execute(sql, {
                "id_aset": int(raw_data['id_aset']),
                "aktivitas": raw_data['aktivitas'],
                "ket": raw_data.get('keterangan', ''),
                "user": raw_data.get('pengguna', 'Petugas')
            })
            resp.media = {"status": "success", "message": "Aktivitas aset berhasil dicatat"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp):
        """Update Data Riwayat"""
        raw_data = req.get_media()
        try:
            sql = """
                UPDATE riwayat_aset SET 
                id_aset=$id_aset, aktivitas=$aktivitas, keterangan=$ket, pengguna=$user
                WHERE id=$id
            """
            db.execute(sql, {
                "id": int(raw_data['id']),
                "id_aset": int(raw_data['id_aset']),
                "aktivitas": raw_data['aktivitas'],
                "ket": raw_data['keterangan'],
                "user": raw_data['pengguna']
            })
            resp.media = {"status": "success", "message": "Catatan riwayat berhasil diperbarui"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus Log Riwayat"""
        id_riwayat = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM riwayat_aset WHERE id = $id", {"id": id_riwayat})
            resp.media = {"status": "success", "message": "Catatan riwayat berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}