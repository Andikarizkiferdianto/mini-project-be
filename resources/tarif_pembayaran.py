import falcon
from pony.orm import db_session
from models.schema import db


class TarifPembayaranOptionsResource:
    @db_session
    def on_get(self, req, resp):
        try:
            # 1. Ambil Data Kelas
            data_kelas = db.select("id, nama_kelas FROM kelas")
            list_kelas = [{"id": r[0], "nama": r[1]} for r in data_kelas]

            # 2. Ambil Data Tahun Ajaran
            data_ta = db.select("id, nama FROM tahun_ajaran")
            list_ta = [{"id": r[0], "nama": r[1]} for r in data_ta]

            # 3. Ambil Data Jenis Pembayaran (untuk Jenis Bayar & Tipe Bayar)
            data_jp = db.select("id, nama_pembayaran FROM jenis_pembayaran")
            list_jp = [{"id": r[0], "nama": r[1]} for r in data_jp]

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": "success",
                "data": {
                    "kelas": list_kelas,
                    "tahun_ajaran": list_ta,
                    "jenis_pembayaran": list_jp,
                    "tipe_bayar": [
                        {"id": "bulanan", "nama": "Bulanan"},
                        {"id": "bebas", "nama": "Bebas/Cicilan"}
                    ]
                }
            }
        except Exception as e:
            print(f"Error Options: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class ListTarifSiswaResource:
    @db_session
    def on_get(self, req, resp):
        try:
            # Ambil filter dari parameter URL
            kelas_id = req.get_param('kelas_id')

            if not kelas_id:
                resp.status = falcon.HTTP_400
                resp.media = {"status": "error", "message": "Parameter kelas_id wajib diisi"}
                return

            # REVISI: Query dibuat satu baris rata (flat) tanpa enter/spasi aneh
            sql = "SELECT s.nis, s.nama, jp.nama_pembayaran, jp.nominal_ketetapan FROM siswa s JOIN jenis_pembayaran jp WHERE s.kelas = $kelas_id"

            # Jalankan query dengan parameter
            res = db.select(sql, {"kelas_id": kelas_id})

            results = []
            for r in res:
                results.append({
                    "nis": r[0],
                    "nama": r[1],
                    "pembayaran": r[2],
                    "tarif": float(r[3])
                })

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": "success",
                "data": results
            }
        except Exception as e:
            print(f"Error List Tarif: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}