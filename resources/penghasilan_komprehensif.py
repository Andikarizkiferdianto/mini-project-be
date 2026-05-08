import falcon
from models.schema import db
from pony.orm import db_session
import traceback


class PenghasilanKomprehensifResource:
    @db_session
    def on_get(self, req, resp):
        tgl_awal = req.get_param('start')
        tgl_akhir = req.get_param('end')

        if not tgl_awal or not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {
                "status": "error",
                "message": "Parameter 'start' dan 'end' wajib diisi (YYYY-MM-DD)"
            }
            return

        try:
            sql = """SELECT 
kode_akun, 
nama_akun,
SUM(COALESCE(kredit, 0)) - SUM(COALESCE(debet, 0)) as saldo_pendapatan,
SUM(COALESCE(debet, 0)) - SUM(COALESCE(kredit, 0)) as saldo_beban
FROM jurnal
WHERE tanggal >= $tgl_awal AND tanggal <= $tgl_akhir
AND (kode_akun LIKE '4%' OR kode_akun LIKE '5%')
GROUP BY kode_akun, nama_akun
ORDER BY kode_akun ASC"""

            result = db.select(sql)

            pendapatan_list = []
            beban_list = []
            total_pendapatan = 0
            total_beban = 0

            for row in result:
                kode = row[0]
                nama = row[1]

                if kode.startswith('4'):
                    saldo = float(row[2] or 0)
                    total_pendapatan += saldo
                    pendapatan_list.append({
                        "nama_akun": nama,
                        "tanpa_pembatasan": saldo,
                        "dengan_pembatasan": 0,
                        "jumlah": saldo
                    })
                # Filter Akun Beban (Kepala 5)
                elif kode.startswith('5'):
                    saldo = float(row[3] or 0)
                    total_beban += saldo
                    beban_list.append({
                        "nama_akun": nama,
                        "tanpa_pembatasan": saldo,
                        "dengan_pembatasan": 0,
                        "jumlah": saldo
                    })

            resp.media = {
                "status": "success",
                "periode": f"{tgl_awal} s/d {tgl_akhir}",
                "data": {
                    "pendapatan": pendapatan_list,
                    "total_pendapatan": total_pendapatan,
                    "beban": beban_list,
                    "total_beban": total_beban,
                    "laba_rugi_bersih": total_pendapatan - total_beban
                }
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal narik laporan penghasilan komprehensif: {str(e)}"
            }