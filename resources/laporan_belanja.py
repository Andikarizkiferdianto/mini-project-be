import falcon
from pony.orm import db_session, select
from models.schema import TransaksiBelanja

class LaporanBelanjaResource:
    @db_session
    def on_get(self, req, resp):
        tgl_awal = req.get_param('start')
        tgl_akhir = req.get_param('end')

        try:
            sql = "SELECT * FROM transaksi_belanja WHERE tanggal >= $tgl_awal AND tanggal <= $tgl_akhir"

            query = TransaksiBelanja.select_by_sql(sql)

            data = []
            for b in query:
                data.append({
                    "id": b.id,
                    "tanggal": str(b.tanggal),
                    "keterangan": b.keterangan or "",
                    "nominal": float(b.nominal) if b.nominal else 0,
                })

            resp.media = {
                "status": "success",
                "total_items": len(data),
                "data": data
            }
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal narik laporan: {str(e)}"
            }