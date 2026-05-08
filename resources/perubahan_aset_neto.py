import falcon
from models.schema import db
from pony.orm import db_session
import traceback
from datetime import datetime


class PerubahanAsetNetoResource:
    @db_session
    def on_get(self, req, resp):
        tgl_akhir = req.get_param('end')

        if not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "Parameter 'end' wajib diisi"}
            return

        try:
            dt_akhir = datetime.strptime(tgl_akhir, '%Y-%m-%d')
            tgl_akhir_lalu = (dt_akhir.replace(year=dt_akhir.year - 1)).strftime('%Y-%m-%d')
            tgl_awal_tahun = dt_akhir.replace(month=1, day=1).strftime('%Y-%m-%d')

            sql_awal = "SELECT SUM(debet - kredit) FROM jurnal WHERE kode_akun LIKE '3%' AND tanggal <= $tgl_akhir_lalu"
            saldo_awal_raw = db.select(sql_awal)[0]
            saldo_awal = float(saldo_awal_raw or 0) * -1

            sql_surplus = "SELECT SUM(CASE WHEN kode_akun LIKE '4%' THEN (kredit - debet) ELSE 0 END) - SUM(CASE WHEN kode_akun LIKE '5%' THEN (debet - kredit) ELSE 0 END) FROM jurnal WHERE tanggal >= $tgl_awal_tahun AND tanggal <= $tgl_akhir"

            surplus_raw = db.select(sql_surplus)[0]
            surplus_berjalan = float(surplus_raw or 0)

            total_akhir = saldo_awal + surplus_berjalan

            resp.media = {
                "status": "success",
                "tanggal_laporan": tgl_akhir,
                "data": {
                    "periode_lalu": tgl_akhir_lalu,
                    "saldo_awal": saldo_awal,
                    "surplus_berjalan": surplus_berjalan,
                    "total_aset_neto_akhir": total_akhir,
                    "catatan": f"Perubahan aset neto {'menurun' if surplus_berjalan < 0 else 'meningkat'} sebesar Rp {abs(surplus_berjalan)}"
                }
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Gagal hitung aset neto: {str(e)}"}