import falcon
from pony.orm import db_session
from models.schema import db
from datetime import datetime


class LaporanPenerimaanResource:
    @db_session
    def on_get(self, req, resp):
        start_date = req.get_param('start')
        end_date = req.get_param('end')

        try:
            # Query dasar
            sql = "SELECT id, jenis_penerimaan, sumber, nominal, tanggal, menyetujui, keterangan " \
                  "FROM penerimaan WHERE 1=1"

            params = {}

            if start_date:
                sql += " AND tanggal >= $start"
                params['start'] = start_date
            if end_date:
                sql += " AND tanggal <= $end"
                params['end'] = end_date

            sql += " ORDER BY tanggal ASC"

            report_data = db.select(sql, params)

            results = []
            total_nominal = 0
            for r in report_data:
                total_nominal += float(r[3])
                results.append({
                    "id": r[0],
                    "kode_transaksi": f"TRX{r[4].strftime('%Y%m%d')}{r[0]}",
                    "jenis_penerimaan": r[1],
                    "sumber": r[2],
                    "nominal": float(r[3]),
                    "tanggal": r[4].isoformat(),
                    "menyetujui": r[5],
                    "keterangan": r[6]
                })

            resp.media = {
                "status": "success",
                "total_penerimaan": total_nominal,
                "data": results
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}