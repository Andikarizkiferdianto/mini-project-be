import falcon
from models.schema import db
from pony.orm import db_session
import traceback


class PosisiKeuanganResource:
    @db_session
    def on_get(self, req, resp):
        tgl_akhir = req.get_param('end')

        if not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {
                "status": "error",
                "message": "Parameter 'end' (tanggal per) wajib diisi (YYYY-MM-DD)"
            }
            return

        try:
            sql = """SELECT 
kode_akun, 
nama_akun,
SUM(COALESCE(debet, 0)) - SUM(COALESCE(kredit, 0)) as saldo_aset,
SUM(COALESCE(kredit, 0)) - SUM(COALESCE(debet, 0)) as saldo_kewajiban
FROM jurnal
WHERE tanggal <= $tgl_akhir
AND (kode_akun LIKE '1%' OR kode_akun LIKE '2%' OR kode_akun LIKE '3%')
GROUP BY kode_akun, nama_akun
ORDER BY kode_akun ASC"""

            result = db.select(sql)

            aset_list = []
            liabilitas_list = []
            aset_neto_list = []

            total_aset = 0
            total_liabilitas = 0
            total_aset_neto = 0

            for row in result:
                kode = row[0]
                nama = row[1]

                if kode.startswith('1'):
                    saldo = float(row[2] or 0)
                    total_aset += saldo
                    aset_list.append({"nama_akun": nama, "jumlah": saldo})

                elif kode.startswith('2'):
                    saldo = float(row[3] or 0)
                    total_liabilitas += saldo
                    liabilitas_list.append({"nama_akun": nama, "jumlah": saldo})

                elif kode.startswith('3'):
                    saldo = float(row[3] or 0)
                    total_aset_neto += saldo
                    aset_neto_list.append({"nama_akun": nama, "jumlah": saldo})

            resp.media = {
                "status": "success",
                "tanggal_per": tgl_akhir,
                "data": {
                    "aset": {
                        "items": aset_list,
                        "total": total_aset
                    },
                    "liabilitas": {
                        "items": liabilitas_list,
                        "total": total_liabilitas
                    },
                    "aset_neto": {
                        "items": aset_neto_list,
                        "total": total_aset_neto
                    },
                    "total_liabilitas_dan_aset_neto": total_liabilitas + total_aset_neto
                }
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal narik laporan posisi keuangan: {str(e)}"
            }