import falcon
import json
from pony.orm import db_session
from models.schema import db


class RekapBulananResource:
    @db_session
    def on_get(self, req, resp):
        try:
            # Ambil parameter dari URL
            kelas_id = req.get_param('kelas_id')
            jenis_bayar = req.get_param('jenis_bayar_id')

            # REVISI: Gunakan query satu baris agar tidak ada error syntax 1064
            if kelas_id and kelas_id != 'semua':
                sql = "SELECT MONTH(bt.tanggal_bayar), SUM(bt.nominal) FROM bayar_tagihan bt JOIN siswa s ON bt.siswa = s.id WHERE bt.jenis_pembayaran = $jenis_bayar AND s.kelas = $kelas_id GROUP BY MONTH(bt.tanggal_bayar)"
                params = {"jenis_bayar": jenis_bayar, "kelas_id": kelas_id}
            else:
                sql = "SELECT MONTH(tanggal_bayar), SUM(nominal) FROM bayar_tagihan WHERE jenis_pembayaran = $jenis_bayar GROUP BY MONTH(tanggal_bayar)"
                params = {"jenis_bayar": jenis_bayar}

            res = db.select(sql, params)

            nama_bulan = {
                1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
                7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
            }

            results = []
            for r in res:
                results.append({
                    "bulan": nama_bulan.get(r[0], "Unknown"),
                    "total_masuk": float(r[1])
                })

            resp.status = falcon.HTTP_200
            resp.media = {"status": "success", "data": results}

        except Exception as e:
            print(f"Error Rekap: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}