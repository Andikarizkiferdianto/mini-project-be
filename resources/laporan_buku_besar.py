import falcon
from models.schema import Jurnal
from pony.orm import db_session
import traceback


class LaporanBukuBesarResource:
    @db_session
    def on_get(self, req, resp):
        # Ambil parameter dari URL
        kode_akun = req.get_param('kode_akun')
        tgl_awal = req.get_param('start')
        tgl_akhir = req.get_param('end')

        if not kode_akun or not tgl_awal or not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {
                "status": "error",
                "message": "Parameter 'kode_akun', 'start', dan 'end' wajib diisi"
            }
            return

        try:
            sql = """
                SELECT * FROM jurnal 
                WHERE kode_akun = $kode_akun 
                AND tanggal >= $tgl_awal 
                AND tanggal <= $tgl_akhir 
                ORDER BY tanggal ASC, id ASC
            """

            query = Jurnal.select_by_sql(sql)

            data = []
            total_debet = 0
            total_kredit = 0
            saldo_berjalan = 0

            for j in query:
                debet = float(j.debet or 0)
                kredit = float(j.kredit or 0)

                saldo_berjalan += (debet - kredit)

                total_debet += debet
                total_kredit += kredit

                data.append({
                    "id": j.id,
                    "tanggal": str(j.tanggal),
                    "keterangan": j.keterangan or "",
                    "debet": debet,
                    "kredit": kredit,
                    "saldo": saldo_berjalan
                })

            resp.media = {
                "status": "success",
                "info": {
                    "kode_akun": kode_akun,
                    "periode": f"{tgl_awal} s/d {tgl_akhir}",
                    "summary": {
                        "total_debet": total_debet,
                        "total_kredit": total_kredit,
                        "saldo_akhir": saldo_berjalan
                    }
                },
                "data": data
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal narik buku besar: {str(e)}"
            }