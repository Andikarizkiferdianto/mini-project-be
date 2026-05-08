import falcon
from models.schema import Jurnal
from pony.orm import db_session
import traceback


class LaporanJurnalResource:
    @db_session
    def on_get(self, req, resp):
        tgl_awal = req.get_param('start')
        tgl_akhir = req.get_param('end')

        if not tgl_awal or not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {
                "status": "error",
                "message": "Parameter 'start' dan 'end' (YYYY-MM-DD) wajib diisi"
            }
            return

        try:
            sql = "SELECT * FROM jurnal WHERE tanggal >= $tgl_awal AND tanggal <= $tgl_akhir ORDER BY tanggal ASC"

            query = Jurnal.select_by_sql(sql)

            data = []
            for j in query:
                data.append({
                    "id": j.id,
                    "tanggal": str(j.tanggal),
                    "keterangan": j.keterangan or "",
                    "kode_akun": j.kode_akun,
                    "nama_akun": j.nama_akun,
                    "debet": float(j.debet),
                    "kredit": float(j.kredit),
                    "status": j.status
                })

            resp.media = {
                "status": "success",
                "total_data": len(data),
                "data": data
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal narik laporan jurnal: {str(e)}"
            }