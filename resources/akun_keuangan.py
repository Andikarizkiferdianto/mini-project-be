import falcon
from models.schema import db
from pony.orm import db_session
import traceback

class AkunKeuanganResource:
    @db_session
    def on_get(self, req, resp, akun_id=None):
        """Menampilkan daftar akun keuangan"""
        try:
            sql = "SELECT id, akun_id, nomor_rekening, kategori, jenis_arus_kas, keterangan FROM akun_keuangan ORDER BY id DESC"
            result = db.select(sql)
            data = []
            for row in result:
                data.append({
                    "id": row[0],
                    "akun_id": row[1],
                    "nomor_rekening": row[2],
                    "kategori": row[3],
                    "jenis_arus_kas": row[4],
                    "keterangan": row[5]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Gagal narik list: {str(e)}"}

    @db_session
    def on_post(self, req, resp):
        """Tambah Akun Keuangan Baru"""
        raw_data = req.get_media()
        try:
            sql = "INSERT INTO akun_keuangan (akun_id, nomor_rekening, kategori, jenis_arus_kas, keterangan) VALUES ($akun_id, $no_rek, $kat, $arus, $ket)"
            db.execute(sql, {
                "akun_id": raw_data['akun_id'],
                "no_rek": raw_data.get('nomor_rekening', ''),
                "kat": raw_data['kategori'],
                "arus": raw_data.get('jenis_arus_kas', 'Operasi'),
                "ket": raw_data.get('keterangan', '')
            })
            resp.media = {"status": "success", "message": "Akun keuangan berhasil disimpan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp, akun_id):
        """Update Akun Keuangan berdasarkan ID"""
        raw_data = req.get_media()
        try:
            sql = "UPDATE akun_keuangan SET akun_id = $akun_id, nomor_rekening = $no_rek, kategori = $kat, jenis_arus_kas = $arus, keterangan = $ket WHERE id = $id"
            db.execute(sql, {
                "akun_id": raw_data['akun_id'],
                "no_rek": raw_data.get('nomor_rekening', ''),
                "kat": raw_data['kategori'],
                "arus": raw_data.get('jenis_arus_kas', 'Operasi'),
                "ket": raw_data.get('keterangan', ''),
                "id": akun_id
            })
            resp.media = {"status": "success", "message": "Akun keuangan berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, akun_id):
        """Hapus Akun Keuangan berdasarkan ID"""
        try:
            sql = "DELETE FROM akun_keuangan WHERE id = $id"
            db.execute(sql, {"id": akun_id})
            resp.media = {"status": "success", "message": "Akun keuangan berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

class OptionKeuanganResource:
    @db_session
    def on_get(self, req, resp):
        """Endpoint untuk isi dropdown Tambah Akun"""
        try:
            list_master = db.select("SELECT id, kode_akun, nama_akun FROM masterdata")
            resp.media = {
                "status": "success",
                "options": {
                    "master_akun": [{"id": r[0], "label": f"{r[1]} - {r[2]}"} for r in list_master],
                    "kategori": ["KAS", "BANK"],
                    "jenis_arus_kas": ["Operasi", "Investasi", "Pendanaan"]
                }
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}