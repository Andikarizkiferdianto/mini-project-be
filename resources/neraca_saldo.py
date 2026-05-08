import falcon
from models.schema import db, Jurnal, JenisBelanja
from pony.orm import db_session
import traceback


class NeracaSaldoResource:
    @db_session
    def on_get(self, req, resp):
        tgl_akhir = req.get_param('end')

        if not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {
                "status": "error",
                "message": "Parameter 'end' (tanggal akhir) wajib diisi"
            }
            return

        try:
            sql = """SELECT 
jb.kode_akun, 
jb.nama_akun,
SUM(COALESCE(j.debet, 0)) as total_debet,
SUM(COALESCE(j.kredit, 0)) as total_kredit
FROM jenis_belanja jb
LEFT JOIN jurnal j ON jb.kode_akun = j.kode_akun AND j.tanggal <= $tgl_akhir
GROUP BY jb.kode_akun, jb.nama_akun
ORDER BY jb.kode_akun ASC"""

            result = db.select(sql)

            data = []
            grand_total_debet = 0
            grand_total_kredit = 0

            for row in result:

                debet = float(row[2] or 0)
                kredit = float(row[3] or 0)

                grand_total_debet += debet
                grand_total_kredit += kredit

                data.append({
                    "kode_akun": row[0],
                    "nama_akun": row[1],
                    "debet": debet,
                    "kredit": kredit
                })

            resp.media = {
                "status": "success",
                "summary": {
                    "periode_sampai": tgl_akhir,
                    "grand_total_debet": grand_total_debet,
                    "grand_total_kredit": grand_total_kredit,
                    "is_balanced": round(grand_total_debet, 2) == round(grand_total_kredit, 2)
                },
                "data": data
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal narik neraca saldo: {str(e)}"
            }