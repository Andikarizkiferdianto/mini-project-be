from pony.orm import db_session
from models.schema import db

class AkunKeuanganResource:
    @db_session
    def on_get(self, req, resp, akun_id=None):
        result = db.select("SELECT id, akun_id, nomor_rekening, kategori, jenis_arus_kas, keterangan FROM akun_keuangan ORDER BY id DESC")
        data = [{"id": r[0], "akun_id": r[1], "nomor_rekening": r[2], "kategori": r[3], "jenis_arus_kas": r[4], "keterangan": r[5]} for r in result]
        resp.media = {"status": "success", "data": data}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        db.execute("INSERT INTO akun_keuangan (akun_id, nomor_rekening, kategori, jenis_arus_kas, keterangan) VALUES ($a, $n, $k, $j, $t)",
                   {"a": data.get('akun_id'), "n": data.get('nomor_rekening'), "k": data.get('kategori'), "j": data.get('jenis_arus_kas'), "t": data.get('keterangan', '')})
        resp.media = {"status": "success", "message": "Berhasil"}

    @db_session
    def on_put(self, req, resp, akun_id):
        data = req.media
        db.execute("UPDATE akun_keuangan SET akun_id=$a, nomor_rekening=$n, kategori=$k, jenis_arus_kas=$j, keterangan=$t WHERE id=$id",
                   {"a": data.get('akun_id'), "n": data.get('nomor_rekening'), "k": data.get('kategori'), "j": data.get('jenis_arus_kas'), "t": data.get('keterangan', ''), "id": akun_id})
        resp.media = {"status": "success", "message": "Berhasil"}

    @db_session
    def on_delete(self, req, resp, akun_id):
        db.execute("DELETE FROM akun_keuangan WHERE id = $id", {"id": akun_id})
        resp.media = {"status": "success", "message": "Berhasil"}

class OptionKeuanganResource:
    @db_session
    def on_get(self, req, resp):
        resp.media = {
            "status": "success",
            "options": {
                "kategori": ["KAS", "BANK"],
                "jenis_arus_kas": ["Operasi", "Investasi", "Pendanaan"]
            }
        }