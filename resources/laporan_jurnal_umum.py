import falcon
from models.schema import db, Jurnal
from pony.orm import db_session
import traceback


class JurnalUmumResource:
    @db_session
    def on_get(self, req, resp):
        tgl_awal = req.get_param('start')
        tgl_akhir = req.get_param('end')

        if not tgl_awal or not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "Parameter 'start' dan 'end' wajib diisi"}
            return

        try:
            sql = """SELECT tanggal, keterangan, kode_akun, nama_akun, debet, kredit, 'Jurnal Manual' as sumber
FROM jurnal
WHERE tanggal >= $tgl_awal AND tanggal <= $tgl_akhir
ORDER BY tanggal ASC"""

            result = db.select(sql)

            data = []
            total_debet = 0
            total_kredit = 0

            for row in result:
                d = float(row[4] or 0)
                k = float(row[5] or 0)
                total_debet += d
                total_kredit += k

                data.append({
                    "tanggal": str(row[0]),
                    "keterangan": row[1],
                    "kode_akun": row[2],
                    "nama_akun": row[3],
                    "debet": d,
                    "kredit": k,
                    "sumber": row[6]
                })

            resp.media = {
                "status": "success",
                "summary": {
                    "total_debet": total_debet,
                    "total_kredit": total_kredit,
                    "is_balanced": round(total_debet, 2) == round(total_kredit, 2)
                },
                "data": data
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}