import json
import falcon
from pony.orm import db_session
from models.schema import db, BayarTagihan, JenisPembayaran


class DashboardKeuanganResource:
    @db_session
    def on_get(self, req, resp):
        try:
            bulan_list = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]

            # 1. Ambil JenisPembayaran
            jenis_data = db.select("id, nama_pembayaran FROM jenis_pembayaran")

            realisasi_tabel = []
            for row in jenis_data:
                jp_id = row[0]
                nama_pembayaran = row[1]

                item = {"kategori": nama_pembayaran}
                total_kategori = 0

                for m in bulan_list:
                    # PERBAIKAN: Gunakan [0] untuk mengambil hasil SUM, bukan .get()
                    sql_sum = "SELECT SUM(nominal) FROM bayar_tagihan WHERE jenis_pembayaran = $jp_id AND MONTH(tanggal_bayar) = $m"
                    res_sum = db.select(sql_sum)[0]
                    sum_bulan = res_sum if res_sum else 0

                    item[f"m_{m}"] = float(sum_bulan)
                    total_kategori += float(sum_bulan)

                item["total"] = total_kategori
                realisasi_tabel.append(item)

            # 2. Grafik Bulanan Keseluruhan
            grafik_pembayaran = []
            for m in bulan_list:
                # PERBAIKAN: Gunakan [0] juga di sini
                sql_grafik = "SELECT SUM(nominal) FROM bayar_tagihan WHERE MONTH(tanggal_bayar) = $m"
                res_grafik = db.select(sql_grafik)[0]
                sum_m = res_grafik if res_grafik else 0
                grafik_pembayaran.append(float(sum_m))

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": "success",
                "data": {
                    "realisasi_tabel": realisasi_tabel,
                    "grafik_pembayaran": grafik_pembayaran
                }
            }

        except Exception as e:
            print(f"Error Dashboard: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}